from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
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


#Creating vector for a specific role
def create_vector_store_by_role(docs, role):   
    embedding=OpenAIEmbeddings()
    persist_directory="chroma_db"

    logging.info(f"Creating Chroma vectorstore for collection: {role} ...... ")

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory,
        collection_name=role
    )

    logging.info(f"Creating Chroma vectorstore for collection: {role} success")
    logging.info("-----------------------------------------------------------------------------------------------------------------")





