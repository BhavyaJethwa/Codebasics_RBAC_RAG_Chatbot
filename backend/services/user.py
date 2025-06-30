from fastapi import APIRouter, HTTPException, status
from schemas.UserCreate import UserCreate
from utils.register import register_user
from utils.database import init_db
router = APIRouter(tags=["User"])

# API to register users.
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    try:
        register_user(user.name, user.username, user.password, user.role)
        return {"message": f"User {user.username} registered successfully as {user.role}."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
