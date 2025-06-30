from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from utils.database import get_db_connection

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, password, role FROM users WHERE username = ?", (credentials.username,))
        row = cursor.fetchone()
        if not row or not bcrypt.verify(credentials.password, row[1]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": credentials.username, "role": row[2], "name":row[0]}


