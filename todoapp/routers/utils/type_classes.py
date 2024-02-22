from pydantic import BaseModel, Field


class Todo_Request(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., ge=0, le=5)
    completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Now to do chores",
                "description": "Wash the clothes and hang them to dry",
                "priority": 3,
                "completed": False,
            }
        }


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "anonymous",
                "email": "anonymous@gmail.com",
                "first_name": "anonymous_first_name",
                "last_name": "anonymous_last_name",
                "password": "password",
                "role": "user",
            }
        }
