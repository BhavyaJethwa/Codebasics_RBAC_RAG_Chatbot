from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from RAG.get_retriever import get_retriever_by_role
from dotenv import load_dotenv
load_dotenv()

rewrite_query_system_template = (
    
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."

)

rewrite_query_prompt = ChatPromptTemplate.from_messages([
    ("system", rewrite_query_system_template),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant.The user may ask vague questions,use the following context to answer the user's question, give context aware responses only. If the question is too vague, politely ask for clarification."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")])

#Creating RAG Chain according to role. Default settings are model="gpt-4o-mini" and role="employee"
def rag_chain_by_role(model="gpt-4o-mini", role="employee"):
    llm = ChatOpenAI(model=model)
    retriever = get_retriever_by_role(role)
    history_aware_retriever = create_history_aware_retriever(llm=llm,prompt=rewrite_query_prompt,retriever=retriever)
    qa_chain = create_stuff_documents_chain(llm,qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever,qa_chain)
    return rag_chain
