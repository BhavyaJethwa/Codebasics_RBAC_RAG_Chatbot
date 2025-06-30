import os
from utils.database import get_db_connection, get_roles
from RAG.data_loader import load_csv, load_markdown, load_pdf, load_text, load_docx
from RAG.create_vectorstore import create_vector_store_by_role
from typing import List
from utils.database import init_db
init_db()
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(filename='app.log',
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    filemode="a",
                    level=logging.INFO)

logging.getLogger("passlib").setLevel(logging.ERROR)

# Suppress HTTP request logs from libraries like httpcore/httpx/openai
for noisy_logger in ["httpx", "https", "httpcore", "openai"]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

#Loading document by a specific role
def load_documents_by_role(role: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
    "SELECT folder_name FROM roles WHERE role = ? AND folder_name is NOT NULL",
    (role,)
)

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


#Creating vectore store for roles.
def create_vector_store(roles:List):

    documents_by_role = {}
    for role in roles:
        logging.info("===============================================================================================================")
        logging.info(f"Loading document for {role} ............................. ")
        documents_by_role[role] = load_documents_by_role(role)
        logging.info(f"Loading document for {role} complete")
        logging.info("===============================================================================================================")

    for role , docs in documents_by_role.items():
        logging.info(role.upper(), ":-")
        logging.info("Total Documents passed: ",len(docs))
        create_vector_store_by_role(docs=docs, role=role)

    logging.info("===============================================================================================================")
    logging.info("Creating executive vector store by merging all role documents...")
    executive_docs = []
    for role_docs in documents_by_role.values():
        executive_docs.extend(role_docs)

    logging.info("EXECUTIVE :-")
    logging.info("Total Documents passed: ", len(executive_docs))
    create_vector_store_by_role(docs=executive_docs, role="executive")
    logging.info("Executive vector store creation complete.")
    logging.info("===============================================================================================================")


roles = get_roles()
create_vector_store(roles)