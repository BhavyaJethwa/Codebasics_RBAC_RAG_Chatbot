from pydantic import BaseModel

class PasswordReset(BaseModel):
    username: str
    new_password: str