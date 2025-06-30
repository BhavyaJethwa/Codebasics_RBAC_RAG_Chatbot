# from fastapi import FastAPI, Depends, HTTPException, status, File, Form, UploadFile
# from schemas.UserCreate import UserCreate
# from schemas.UserQuery import ChatRequest
# from schemas.RoleCreate import RoleCreate
# from schemas.PasswordReset import PasswordReset
# from utils.database import init_db, get_chat_history, insert_application_logs, add_role, get_db_connection, get_roles, cleanup_old_chat_per_session
# init_db()
# from utils.auth import authenticate
# from utils.register import register_user, reset_password
# from rag_chain import rag_chain_by_role
# from update_vector_store import update_vector_store_by_role
# from typing import List
# import asyncio
# import shutil
# import uuid
# import os
# from dotenv import load_dotenv
# import logging 
# logging.basicConfig(filename='app.log', level = logging.INFO)
# load_dotenv()

# app = FastAPI()

# @app.on_event("startup")
# async def start_background_tasks():
#     asyncio.create_task(cleanup_old_chat_per_session())


# @app.get("/")
# def home():
#     return "Codebasics RBAC"


# @app.get("/get_roles")
# def get_roles_from_db():
#     roles = get_roles()
#     return [{"role": role} for role in roles]


# @app.post("/register", status_code=status.HTTP_201_CREATED)
# def register(user: UserCreate):
#     try:
#         register_user(user.name,user.username, user.password, user.role)
#         return {"message": f"User {user.username} registered successfully as {user.role}."}
#     except ValueError as e:
#         # For example: "Username already exists"
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# @app.get("/login", status_code=status.HTTP_200_OK)
# def login(user=Depends(authenticate)):
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     return {
#         "name" : user["name"],
#         "role": user["role"],
#         "is_admin": user["role"] == "admin"
#     }

# @app.post("/reset_password", status_code=status.HTTP_200_OK)
# def reset_user_password(reset: PasswordReset, user=Depends(authenticate)):
#     if user["role"] != "admin":
#         raise HTTPException(status_code=403, detail="Only admins can reset passwords")
#     try:
#         reset_password(reset.username, reset.new_password)
#         return {"message": f"Password for user '{reset.username}' reset successfully."}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))


# @app.post("/add_role", status_code=status.HTTP_201_CREATED)
# def add_role_to_db(role_:RoleCreate):
#     add_role(role_.role, role_.folder_name)
#     return {"message": f"Role '{role_.role}' with folder '{role_.folder_name}' added successfully."}


# @app.post("/add_docs_role")
# def add_docs_for_role(role: str = Form(...), files: List[UploadFile] = File(...)):
#     # --- Get folder_name from DB ---
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT folder_name FROM roles WHERE role = ?", (role,))
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail=f"Role '{role}' not found")

#     folder_name = row[0]
#     folder_path = os.path.join("resources/data", folder_name)
#     os.makedirs(folder_path, exist_ok=True)

#     # --- Save uploaded files ---
#     saved_files = []
#     for file in files:
#         dest_path = os.path.join(folder_path, file.filename)
#         try:
#             with open(dest_path, "wb") as f:
#                 shutil.copyfileobj(file.file, f)
#             saved_files.append(file.filename)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to save {file.filename}: {e}")
    
#     update_vector_store_by_role(role)


#     return {
#         "message": f"{len(saved_files)} files uploaded for role '{role}'",
#         "saved_files": saved_files
#     }
    



# @app.post("/chat")
# def chat(ChatQuery:ChatRequest,user=Depends(authenticate)):
#     if user["role"] != ChatQuery.role:
#         raise HTTPException(status_code=403, detail="Access denied for this role.")
#     session_id = ChatQuery.session_id
#     logging.info(f"session_id: {session_id}, User Query: {ChatQuery.query}")
#     if session_id is None:
#         session_id = str(uuid.uuid4())
    
#     chat_history = get_chat_history(session_id=session_id)
#     rag = rag_chain_by_role(role=user["role"])
#     answer = rag.invoke({
#         "input": ChatQuery.query,
#         "chat_history": chat_history
#     })

#     insert_application_logs(session_id, ChatQuery.query, answer["answer"])
#     logging.info(f"session_id: {session_id}, AI Response: {answer["answer"]}")

#     source_docs = []
#     doc_len  = len(answer['context'])
#     for i in range(0,doc_len):
#         source_docs.append(answer['context'][i].metadata['source'].split("\\")[-1])
#         print(answer['context'][i].metadata['source'].split("\\")[-1])

#     docs = list(set(source_docs))

#     return {
#         "response" : answer['answer'],
#         "sources" : docs,
#         "session_id": session_id
#     }
