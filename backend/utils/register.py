from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic
from passlib.context import CryptContext
from utils.database import get_db_connection
import sqlite3
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

# Function to register users.
def register_user(name:str, username: str, password: str, role: str):
    hashed_password = bcrypt.hash(password)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)",
                (name, username, hashed_password, role)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Username already exists")

#Function to reset password  
def reset_password(username: str, new_password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        raise ValueError("Username not found")

    # Hash the new password
    hashed_password = bcrypt.hash(new_password)

    # Update password
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()

