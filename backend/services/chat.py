from fastapi import APIRouter, Depends, HTTPException
from schemas.UserQuery import ChatRequest
from utils.auth import authenticate
from utils.database import get_chat_history, insert_application_logs
from RAG.rag_chain import rag_chain_by_role
import uuid, logging

router = APIRouter(tags=["Chat"])

#Chat API
@router.post("/chat")
def chat(ChatQuery: ChatRequest, user=Depends(authenticate)):
    if user["role"] != ChatQuery.role:
        raise HTTPException(status_code=403, detail="Access denied for this role.")

    session_id = ChatQuery.session_id or str(uuid.uuid4())
    logging.info(f"session_id: {session_id}, User Query: {ChatQuery.query}")

    chat_history = get_chat_history(session_id=session_id)
    rag = rag_chain_by_role(role=user["role"])
    answer = rag.invoke({
        "input": ChatQuery.query,
        "chat_history": chat_history
    })

    insert_application_logs(session_id, ChatQuery.query, answer["answer"])
    logging.info(f"session_id: {session_id}, AI Response: {answer['answer']}")

    source_docs = []
    doc_len  = len(answer['context'])
    for i in range(0,doc_len):
        source_docs.append(answer['context'][i].metadata['source'].split("\\")[-1])
        print(answer['context'][i].metadata['source'].split("\\")[-1])

    docs = list(set(source_docs))

    return {
        "response": answer['answer'],
        "sources": docs,
        "session_id": session_id
    }
