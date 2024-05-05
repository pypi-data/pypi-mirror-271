from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def IndexFromWebPages(pages: list[str], embeddings,vectorstore, chunk_size: int = 2000):
    """
    ### Load pdf from folder
    This function loads documents from a folder and creates a Fass index (db).\n
    - pages: webpage ('https') to load inside index\n
    - chunk_size: Chunk size in characters (default 2000)\n
    - embeddings: Embeddings object from langchain.embeddings\n
    - vectorstore: could be FAISS or ChromaDB\n
    """

    documents = []
    # Process each PDF file and split into chunks of 24000 characters
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0, length_function=len, is_separator_regex=False) # FIXED

    super_text = ""
    documents = []

    # Example usage
    for page in tqdm(pages, "Parsing pages"):
        html_content = requests.get(page).text
        soup = BeautifulSoup(html_content, "html.parser")
        if soup.title != None:
            title = soup.title.text.replace("/","-")
            elements = soup.find_all("body") # Get all body elements (IMP) otherwise it retrieve all the html code
            for element in elements:
                super_text += element.get_text()  
            print(f"Page '{title}' ingested")
        else:
            print(f"--> X '{page}' gave error")
    
    texts = text_splitter.split_text(super_text)

    for text in texts:
        document = Document(page_content=text, metadata={"title": title, "link": page, "type": "site"})
        documents.append(document)

    # Store Embeddings in FAISS
    for i in tqdm(range(0,1), "Creating db from documents"):
        db = vectorstore.from_documents(documents, embeddings)
    return db
