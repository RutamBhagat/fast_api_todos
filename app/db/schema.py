from typing import Optional
from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., ge=0, le=5)
    is_completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Now to do chores",
                "description": "Wash the clothes and hang them to dry",
                "priority": 3,
                "is_completed": False,
            }
        }

# User inside TodoDisplay
class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: str

    class Config:
        orm_mode = True

class TodoDisplay(BaseModel):
    title: str
    description: str
    priority: int
    is_completed: bool
    owner: User

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)
    role: str = "user"
    phone_number: str = Field(..., min_length=10, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "anonymous",
                "email": "anonymous@gmail.com",
                "first_name": "anonymous_first_name",
                "last_name": "anonymous_last_name",
                "password": "password",
                "role": "user",
                "phone_number": "1234567890",
            }
        }


class ChangePasswordBase(BaseModel):
    password: str
    new_password: str = Field(..., min_length=6, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "password": "password",
                "new_password": "new_password",
            }
        }


class AddressBase(BaseModel):
    address1: str = Field(..., min_length=1, max_length=50)
    address2: str = Field(..., min_length=1, max_length=50)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    country: str = Field(..., min_length=1, max_length=50)
    postalcode: str = Field(..., min_length=1, max_length=50)
    apt_num: Optional[str] = Field(None, min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "address1": "1234 Main St",
                "address2": "Apt 123",
                "city": "Anytown",
                "state": "New York",
                "country": "USA",
                "postalcode": "12345",
                "apt_num": "Apt 123",
            }
        }
