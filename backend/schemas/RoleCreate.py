from pydantic import BaseModel

class RoleCreate(BaseModel):
    role: str
    folder_name: str