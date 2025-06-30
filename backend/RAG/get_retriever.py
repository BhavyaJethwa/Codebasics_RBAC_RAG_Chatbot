from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import logging
logging.basicConfig(filename='rag_chain.log',
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    filemode="a",
                    level=logging.INFO)
# Suppress HTTP request logs from libraries like httpcore/httpx/openai
for noisy_logger in ["httpx", "https", "httpcore", "openai"]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)



def get_retriever_by_role(role):
    if role == "admin" or role == "Admin":
        role = "executive"
        logging.info("Getting Executive retriever")
    
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=OpenAIEmbeddings(),
        collection_name=role
    )
    logging.info(f"VectorDB for {role} fetched - success")

    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    logging.info(f"Retriever for {role} fetched - success")
    return retriever
