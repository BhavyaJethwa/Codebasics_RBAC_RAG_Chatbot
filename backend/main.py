from fastapi import FastAPI
import asyncio
from utils.database import cleanup_old_chat_per_session, init_db
from services import auth, user, role, chat
import logging

logging.basicConfig(filename='app.log',
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    filemode="a",
                    level=logging.INFO)
logging.getLogger("passlib").setLevel(logging.ERROR)
# Suppress HTTP request logs from libraries like httpcore/httpx/openai
for noisy_logger in ["httpx", "https", "httpcore", "openai"]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

init_db()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_old_chat_per_session())

# Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(chat.router)



