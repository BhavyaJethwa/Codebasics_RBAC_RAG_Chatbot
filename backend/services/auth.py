from fastapi import APIRouter, Depends, HTTPException, status
from utils.auth import authenticate
from utils.register import reset_password
from schemas.PasswordReset import PasswordReset

router = APIRouter(tags=["Auth"])

#Login API
@router.get("/login", status_code=status.HTTP_200_OK)
def login(user=Depends(authenticate)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "name": user["name"],
        "role": user["role"],
        "is_admin": user["role"] == "admin"
    }

#Password reset API
@router.post("/reset_password", status_code=status.HTTP_200_OK)
def reset_user_password(reset: PasswordReset, user=Depends(authenticate)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can reset passwords")
    try:
        reset_password(reset.username, reset.new_password)
        return {"message": f"Password for user '{reset.username}' reset successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
