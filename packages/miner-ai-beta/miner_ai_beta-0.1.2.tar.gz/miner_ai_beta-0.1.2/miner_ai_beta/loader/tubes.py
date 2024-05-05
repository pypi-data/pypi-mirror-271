from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
from tqdm import tqdm

def IndexFromTubes(tubes: list[str], embeddings, vectorstore, chunk_size: int = 2000):
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

    
    documents = []
    total_text = ""

    # Example usage
    for tube in tqdm(tubes,"Parsing videos"):
        title = YouTube(tube).title
        tube_id = tube.split("https://www.youtube.com/watch?v=")[1] 
        transcripts = YouTubeTranscriptApi.get_transcript(tube_id)
        for transcript in transcripts:
            time = datetime.timedelta(0,transcript["start"])
            current_text = transcript["text"]
            total_text += f"text: {current_text}, at: {time}\n"
    texts = text_splitter.split_text(total_text)

    for text in texts:
        document = Document(page_content=text, metadata={"title": title, "link": tube, "type": "video"})
        documents.append(document)


    # Store Embeddings in FAISS
    for i in tqdm(range(0,1), "Creating db from documents"):
        db = vectorstore.from_documents(documents, embeddings)
    return db
