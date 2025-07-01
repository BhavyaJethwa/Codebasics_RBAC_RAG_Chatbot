import sqlite3
import asyncio
from utils.message_trimmer import trim_chat_history
from datetime import datetime, timedelta
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



from passlib.context import CryptContext
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


DB_PATH = "../FinSolve.db"

admin_username = os.getenv("ADMIN_USERNAME", "Admin")
admin_password = os.getenv("ADMIN_PASSWORD", "adminpass")
    
# To get database connection object.
def get_db_connection():
    return sqlite3.connect(DB_PATH)


# Intializing database.
def init_db():
    create_users()
    create_application_logs()
    create_roles()
    insert_user(name="Admin",username=admin_username,password=admin_password, role="admin")

# Function to create users table
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


#Function to create roles table
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

#Function to create application log table used for chat history.
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

#Function to insert role to roles table
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

#Function to insert user into users table
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

#Function to insert into application log table (chat history)
def insert_application_logs(session_id, user_query, llm_response):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO application_logs (session_id, user_query, llm_response, created_at) VALUES (?, ?, ?, ?)",
        (session_id, user_query, llm_response, datetime.utcnow())
    )
    conn.commit()
    conn.close()

# function to get all the roles from roles table
def get_roles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles")
    roles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return roles

# Function to get chat history from application logs table.
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


# Function to cleanup application logs older than 24 hours
async def cleanup_old_chat_per_session():
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Calculate the cutoff timestamp (24 hours ago)
            cutoff_time = datetime.utcnow() - timedelta(hours=24)

            # Delete logs older than 24 hours
            cursor.execute("""
                DELETE FROM application_logs
                WHERE created_at < ?
            """, (cutoff_time,))

            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            logging.info(f"[Cleanup] Deleted {deleted_count} old messages older than 24 hours.")
        except Exception as e:
            logging.error(f"[Cleanup Error] {e}")

        await asyncio.sleep(4 * 60 * 60)  # Run every 4 hours