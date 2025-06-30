import sqlite3
import asyncio
from utils.message_trimmer import trim_chat_history
from datetime import datetime
import logging 
import os
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(filename='app.log',
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    filemode="a",
                    level=logging.INFO)
logging.getLogger("passlib").setLevel(logging.ERROR)

# Suppress HTTP request logs from libraries like httpcore/httpx/openai
for noisy_logger in ["httpx", "https", "httpcore", "openai"]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)
import warnings

# Suppress passlib bcrypt version warnings
warnings.filterwarnings("ignore", message=".*(trapped) error reading bcrypt version*")


from passlib.context import CryptContext
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


DB_PATH = "../FinSolve.db"

admin_username = os.getenv("ADMIN_USERNAME", "Admin")
admin_password = os.getenv("ADMIN_PASSWORD", "adminpass")
    

def get_db_connection():
    return sqlite3.connect(DB_PATH)



def init_db():
    create_users()
    create_application_logs()
    create_roles()
    insert_user(name="Admin",username=admin_username,password=admin_password, role="admin")

def create_users():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def create_roles():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,     
            role TEXT UNIQUE NOT NULL,
            folder_name TEXT 
        )
    ''')
    # List of default roles
    default_roles = ["finance", "human_resource", "marketing", "engineering", "employee","admin"]
    default_folders = ["finance", "hr", "marketing", "engineering", "general"]

    # Insert roles if they don't already exist
    for role, folder_name in zip(default_roles, default_folders):
        cursor.execute("INSERT OR IGNORE INTO roles (role, folder_name) VALUES (?, ?)", (role, folder_name))

    conn.commit()
    conn.close()

def add_role(role, folder_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO roles (role, folder_name) VALUES (?, ?)", (role, folder_name))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Role already exists.")
    finally:
        conn.close()

def insert_user(name:str, username: str, password: str, role: str):
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
            print("User already exists")
            pass

def get_roles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles")
    roles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return roles

def create_application_logs():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS application_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_query TEXT,
        llm_response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )

        """
    )
    conn.close()

def insert_application_logs(session_id, user_query, llm_response):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO application_logs (session_id, user_query, llm_response, created_at) VALUES (?, ?, ?, ?)",
        (session_id, user_query, llm_response, datetime.utcnow())
    )
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_query, llm_response " \
        "FROM application_logs " \
        "WHERE session_id = ? " \
        "ORDER BY created_at", (session_id,)
    )
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role":"human" , "content": row[0]},
            {"role": "ai" , "content" : row[1]}
        ])
    conn.close()
    
    if len(messages) <= 16:
        return messages
    else:
        return trim_chat_history(messages)

RETENTION_LIMIT = 10
async def cleanup_old_chat_per_session():
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get all session_ids
            cursor.execute("SELECT DISTINCT session_id FROM application_logs")
            session_ids = cursor.fetchall()

            total_deleted = 0

            for (session_id,) in session_ids:
                cursor.execute("""
                    SELECT id FROM application_logs
                    WHERE session_id = ?
                    ORDER BY created_at DESC
                    LIMIT -1 OFFSET ?
                """, (session_id, RETENTION_LIMIT))

                ids_to_delete = [row[0] for row in cursor.fetchall()]
                if ids_to_delete:
                    placeholders = ",".join(["?"] * len(ids_to_delete))
                    query = f"DELETE FROM application_logs WHERE id IN ({placeholders})"
                    cursor.execute(query, ids_to_delete)
                    total_deleted += cursor.rowcount

            conn.commit()
            conn.close()

            logging.info(f"[Cleanup] Deleted {total_deleted} old messages (retained last {RETENTION_LIMIT}/session)")
        except Exception as e:
            logging.error(f"[Cleanup Error] {e}")

        await asyncio.sleep(4 * 60 * 60)  # Run every 4 hours