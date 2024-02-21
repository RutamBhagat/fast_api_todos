import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from models import Users
from routers.todos import db_dependency
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


router = APIRouter()


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


class UserLoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {"username": "anonymous", "password": "password"}
        }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    # Check if user already exists, both username and email should be unique
    existing_user = (
        db.query(Users)
        .filter(
            Users.username == create_user_request.username
            or Users.email == create_user_request.email
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    hashed_password = get_password_hash(create_user_request.password)
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=hashed_password,
        role=create_user_request.role,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, user: UserLoginRequest):
    user_model = db.query(Users).filter(Users.username == user.username).first()
    is_password_matching = verify_password(user.password, user_model.hashed_password)

    if not user_model or not is_password_matching:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Define the secret key and the algorithm used to sign the JWT
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")

    # Define the token expiration time
    TOKEN_EXPIRATION_TIME = timedelta(hours=48)

    # Generate the JWT token
    token = jwt.encode(
        {
            "sub": user.username,
            "exp": datetime.utcnow() + TOKEN_EXPIRATION_TIME,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    # Return the token
    return {"access_token": token, "token_type": "bearer"}
