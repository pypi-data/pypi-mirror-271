![Alt text](images\logo\MINER-AI.png)

# Miner AI Beta ⛏️ -- Site under construction

Miner AI Beta is an innovative project designed to index various types of documents and web pages into a searchable database. By leveraging state-of-the-art language models and indexing techniques, Miner AI Beta aims to make information retrieval fast, efficient, and highly relevant.

## Features

- Indexing support for PDFs, PowerPoint presentations, Excel spreadsheets, web pages, and YouTube video transcripts.
- Utilizes powerful embeddings and vector storage mechanisms to create efficient search indexes.
- Merge functionality to combine multiple indexes for comprehensive search capabilities.
- Designed with modularity in mind, allowing for easy extension to support additional document types.

## Installation

Miner AI Beta requires Python 3.12 or later. It is recommended to use a virtual environment to manage the project dependencies.

To install Miner AI Beta and its dependencies, follow these steps:

```bash
# Clone the repository
git clone https://your-repository-url/miner-ai-beta.git
cd miner-ai-beta

# Install dependencies using Poetry
poetry install
```

## Usage

1. **Indexing Documents**

   To start indexing your documents, you need to prepare your documents in the supported formats (PDF, PPTX, XLSX, web pages, YouTube videos).

   Example for indexing PDFs:

   ```python
   from src.pdfs import IndexFromPdfs
   embeddings = ... # Initialize your embeddings model
   vectorstore = ... # Initialize your vector store (FAISS, ChromaDB, etc.)
   folder_path = 'path/to/your/pdfs'

   db = IndexFromPdfs(folder_path, embeddings, vectorstore)
   ```

2. **Merging Indexes**

   If you have multiple indexes that you wish to merge, use the `MergeIndexes` function.

   ```python
   from src.union import MergeIndexes

   db_combined = MergeIndexes([db1, db2, ...])
   ```

3. **Searching**

   To search within your index, you will need to implement a search mechanism that leverages the created indexes.

   Please refer to `vectorstore` documentation for details on querying indexed data.

## Contributing

Contributions are welcome! Feel free to open an issue or pull request if you have suggestions or improvements.

## License

[MIT](LICENSE.md)

---

Remember to replace placeholder texts like `https://your-repository-url/miner-ai-beta.git` with actual information relevant to your project. Also, the `Usage` section should be expanded based on the actual implementation details of searching through the indexes, which would depend significantly on the specifics of the `vectorstore` and `embeddings` implementations your project uses.