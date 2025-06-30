from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings




def create_vector_store_by_role(docs, role):   
    embedding=OpenAIEmbeddings()
    persist_directory="chroma_db"

    print(f"Creating Chroma vectorstore for collection: {role} ...... ")

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory,
        collection_name=role
    )

    # vectorstore.persist()
    print(f"Creating Chroma vectorstore for collection: {role} success")
    print("-----------------------------------------------------------------------------------------------------------------")
    # return vectorstore






