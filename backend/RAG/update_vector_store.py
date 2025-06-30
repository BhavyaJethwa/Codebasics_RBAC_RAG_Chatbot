from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from utils.database import get_db_connection, get_roles
from RAG.data_loader import load_csv, load_markdown, load_pdf, load_text, load_docx
import logging
logging.basicConfig(filename='rag_chain.log',
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    filemode="a",
                    level=logging.INFO)
# Suppress HTTP request logs from libraries like httpcore/httpx/openai
for noisy_logger in ["httpx", "https", "httpcore", "openai"]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)



#Loading documents according to a specific role. 
def load_documents_by_role(role: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT folder_name FROM roles WHERE role = ?", (role,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"No folder mapping found for role '{role}'")

    folder_name = row[0]
    base_path = "resources/data"
    path = os.path.join(base_path, folder_name)

    logging.info("Loading from path:", path)

    docs = []

    if not os.path.exists(path):
        logging.info(f"Path does not exist: {path}")
        return docs  

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        logging.info("file_path:", file_path)

        try:
            loaded_docs = []
            if file_name.endswith(".csv"):
                loaded_docs = load_csv(file_path)
                logging.info(file_name, "CSV Documents loaded:", file_path)
            elif file_name.endswith(".md"):
                loaded_docs = load_markdown(file_path)
                logging.info(file_name, "MD Documents loaded:", file_path)
            elif file_name.endswith(".txt"):
                loaded_docs = load_text(file_path)
                logging.info(file_name, "Text Documents loaded:", file_path)
            elif file_name.endswith(".pdf"):
                loaded_docs = load_pdf(file_path)
                logging.info(file_name, "PDF Documents loaded:", file_path)
            elif file_name.endswith(".docx"):
                loaded_docs = load_docx(file_path)
                logging.info(file_name, "Word Documents loaded:", file_path)
            else:
                continue

            for doc in loaded_docs:
                doc.metadata["source"] = file_path
                doc.metadata["role"] = role.lower()

            docs.extend(loaded_docs)

        except Exception as e:
            logging.info(f"Failed to load {file_path}: {e}")

    logging.info("Total docs loaded:", len(docs))
    return docs

#Updating vector store if new document is added.
def update_vector_store_by_role(role):
    docs = load_documents_by_role(role)
    roles = get_roles()
    embedding=OpenAIEmbeddings()
    persist_directory="chroma_db"
    if role in roles:
        logging.info(f"{role} found. Updating vectorstore.")
        vectorstore = Chroma(
        collection_name=role, 
        embedding_function=embedding,
        persist_directory=persist_directory
        )

        vectorstore.add_documents(docs)

        logging.info(f"Updated vector store for {role} - success")
        logging.info(f"Updating Executive vectorstore")
            
        exe_vectorstore = Chroma(
        collection_name="executive", 
        embedding_function=embedding,
        persist_directory=persist_directory
        )
        
        exe_vectorstore.add_documents(docs)
        logging.info(f"Executive vectorstore updated successfully")

    else:
        logging.info(f"Creating NEW vectorstore for {role}")
        vectorstore = Chroma.from_documents(
                            documents=docs,
                            embedding=embedding,
                            persist_directory=persist_directory,
                            collection_name=role
        )
        logging.info(f"Created vectorstore for {role} - success")
        
        logging.info(f"Updating Executive vectorstore")
        exe_vectorstore = Chroma(
        collection_name="executive", 
        embedding_function=embedding,
        persist_directory=persist_directory
        )

        exe_vectorstore.add_documents(docs)
        logging.info(f"Executive vectorstore updated successfully")
