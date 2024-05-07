# Miner AI Beta ⛏️ -- Library under construction

<p align="center">
  <img src="images\logo\MINER-AI.png" alt="Scrapegraph-ai Logo" style="width: 35%;">
</p>

Miner AI Beta represents a groundbreaking endeavor, specially crafted to compile an assortment of documents and web pages into a searchable database, all achieved offline. Utilizing cutting-edge language models along with sophisticated indexing strategies, Miner AI Beta is uniquely positioned to streamline the retrieval of information, ensuring speed, efficiency, and superior relevance without the need for an online connection.


## 💪 Features

- Indexing support for PDFs, PowerPoint presentations, Excel spreadsheets, web pages, and YouTube video transcripts.
- Utilizes powerful embeddings and vector storage mechanisms to create efficient search indexes.
- Merge functionality to combine multiple indexes for comprehensive search capabilities.
- Designed with modularity in mind, allowing for easy extension to support additional document types.

## 💻 Installation

Miner AI Beta requires Python 3.12 or later. It is recommended to use a virtual environment to manage the project dependencies.

To install Miner AI Beta and its dependencies, follow these steps:

```bash
# Install the library from pipy
pip install miner-ai-beta==<last-code-version>
```

## ⚒️ Usage

1. **Indexing Documents**

   To start indexing your documents, you need to prepare your documents in the supported formats (PDF, PPTX, XLSX, web pages, YouTube videos).

   Example for indexing PDFs:

   ```python
   # Initialize your embeddings model
   from langchain_openai import OpenAIEmbeddings

   embeddings = OpenAIEmbeddings() 

   # Initialize your vector store (FAISS, ChromaDB, etc.)
   from langchain.vectorstores.faiss import FAISS

   vectorstore = FAISS 

   # Index your documents inside the vectorstore
   from miner_ai_beta.loader import IndexFromPdfs
   from miner_ai_beta.loader import IndexFromDocs
   from miner_ai_beta.loader import IndexFromXlss

   folder_path = 'path/to/your/pdfs'

   pdf = IndexFromPdfs(folder_path, embeddings, vectorstore)
   doc = IndexFromDocs(folder_path, embeddings, vectorstore)
   excel = IndexFromXlss(folder_path, embeddings, vectorstore)

   # Merge your indexes
   from miner_ai_beta.loader import MergeIndexes

   final_index = MergeIndexes([pdf, doc, excel])

   # Save your index locally for later use
   final_index.save_local('path/to/your/final/index')
   ```


2. **Searching**

   To search within your index, you will need to implement a search mechanism that leverages the created indexes.

   Please refer to `vectorstore` documentation for details on querying indexed data.

   Example for searching documents:

   ```python
   # After you have saved your index locally, you can load it later
   from langchain_openai import OpenAIEmbeddings
   embeddings = OpenAIEmbeddings() 
   FAISS.load_local('path/to/your/final/index', embeddings, allow_dangerous_deserialization=True)

   # Initialize your vector store as a retriever to retrieve only the first 10 documents that are most relevant to the query
   retriever = db.as_retriever(search_kwargs={"k":10})

   # Retrieve based on query string
   query = "What is the meaning of life?"
   result = retriever.invoke(query)  # returns a list of documents
   ```

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or pull request if you have suggestions or improvements.

## 📜 License

Miner AI Beta is licensed under the MIT License. See the [MIT](LICENSE) file for more information.

## Acknowledgements

- We would like to thank all the contributors to the project and the open-source community for their support.
- Miner AI Beta is meant to be used for ai data mining over documents and research purposes only. We are not responsible for any misuse of the library.