from langchain_community.document_loaders import CSVLoader, PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from langchain.schema import Document

# ------------------ Loaders with Splitters ------------------

def load_csv(file_path):
    loader = CSVLoader(file_path)
    return loader.load()

def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=["\n\n"]
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks]

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks]

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(pages)

def load_docx(file_path):
    loader = UnstructuredWordDocumentLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(pages)



