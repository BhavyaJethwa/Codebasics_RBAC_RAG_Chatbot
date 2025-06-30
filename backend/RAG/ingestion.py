import os
from utils.database import get_db_connection, get_roles
from RAG.data_loader import load_csv, load_markdown, load_pdf, load_text, load_docx
from RAG.create_vectorstore import create_vector_store_by_role
from typing import List
from utils.database import init_db
init_db()
from dotenv import load_dotenv
load_dotenv()


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

    print("Loading from path:", path)

    docs = []

    if not os.path.exists(path):
        print(f"Path does not exist: {path}")
        return docs  

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        print("file_path:", file_path)

        try:
            loaded_docs = []
            if file_name.endswith(".csv"):
                loaded_docs = load_csv(file_path)
                print(file_name, "CSV Documents loaded:", file_path)
            elif file_name.endswith(".md"):
                loaded_docs = load_markdown(file_path)
                print(file_name, "MD Documents loaded:", file_path)
            elif file_name.endswith(".txt"):
                loaded_docs = load_text(file_path)
                print(file_name, "Text Documents loaded:", file_path)
            elif file_name.endswith(".pdf"):
                loaded_docs = load_pdf(file_path)
                print(file_name, "PDF Documents loaded:", file_path)
            elif file_name.endswith(".docx"):
                loaded_docs = load_docx(file_path)
                print(file_name, "Word Documents loaded:", file_path)
            else:
                continue

            for doc in loaded_docs:
                doc.metadata["source"] = file_path
                doc.metadata["role"] = role.lower()

            docs.extend(loaded_docs)

        except Exception as e:
            print(f"Failed to load {file_path}: {e}")

    print("Total docs loaded:", len(docs))
    return docs



def create_vector_store(roles:List):

    documents_by_role = {}
    for role in roles:
        print("===============================================================================================================")
        print(f"Loading document for {role} ............................. ")
        documents_by_role[role] = load_documents_by_role(role)
        print(f"Loading document for {role} complete")
        print("===============================================================================================================")

    for role , docs in documents_by_role.items():
        print(role.upper(), ":-")
        print("Total Documents passed: ",len(docs))
        create_vector_store_by_role(docs=docs, role=role)

    print("===============================================================================================================")
    print("Creating executive vector store by merging all role documents...")
    executive_docs = []
    for role_docs in documents_by_role.values():
        executive_docs.extend(role_docs)

    print("EXECUTIVE :-")
    print("Total Documents passed: ", len(executive_docs))
    create_vector_store_by_role(docs=executive_docs, role="executive")
    print("Executive vector store creation complete.")
    print("===============================================================================================================")


roles = get_roles()
create_vector_store(roles)