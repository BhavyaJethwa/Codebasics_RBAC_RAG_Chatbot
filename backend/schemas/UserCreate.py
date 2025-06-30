from pydantic import BaseModel, Field
from typing import Literal

class UserCreate(BaseModel):
    name: str = Field(..., description="Name of the user.")
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Unique username between 3 and 30 characters",
        example="john_doe"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password with at least 6 characters",
        example="strongPassword123"
    )
    role: str = Field(
        ...,
        description="Role assigned to the user",
        example="engineering"
    )
