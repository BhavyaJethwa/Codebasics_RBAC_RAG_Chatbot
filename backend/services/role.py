from fastapi import APIRouter, HTTPException, Form, File, UploadFile, status
from typing import List
import os, shutil
from utils.database import get_db_connection, get_roles, add_role
from schemas.RoleCreate import RoleCreate
from RAG.update_vector_store import update_vector_store_by_role

router = APIRouter(tags=["Roles"])

@router.get("/get_roles")
def get_roles_from_db():
    roles = get_roles()
    return [{"role": role} for role in roles]

@router.post("/add_role", status_code=status.HTTP_201_CREATED)
def add_role_to_db(role_: RoleCreate):
    add_role(role_.role, role_.folder_name)
    return {"message": f"Role '{role_.role}' with folder '{role_.folder_name}' added successfully."}

@router.post("/add_docs_role")
def add_docs_for_role(role: str = Form(...), files: List[UploadFile] = File(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT folder_name FROM roles WHERE role = ?", (role,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Role '{role}' not found")

    folder_path = os.path.join("resources/data", row[0])
    os.makedirs(folder_path, exist_ok=True)

    saved_files = []
    for file in files:
        dest_path = os.path.join(folder_path, file.filename)
        try:
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            saved_files.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save {file.filename}: {e}")
    
    update_vector_store_by_role(role)
    return {"message": f"{len(saved_files)} files uploaded for role '{role}'", "saved_files": saved_files}
