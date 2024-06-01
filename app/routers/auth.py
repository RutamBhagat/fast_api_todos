from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from app.auth import get_password_hash, verify_password, create_access_token
from app.db.models import DBUsers
from app.db.schema import UserBase
from app.dependencies import db_dependency,login_dependency

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserBase):
    # Check if user already exists, both username and email should be unique
    existing_user = (
        db.query(DBUsers)
        .filter(
            DBUsers.username == create_user_request.username
            or DBUsers.email == create_user_request.email
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    hashed_password = get_password_hash(create_user_request.password)
    new_user = DBUsers(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=hashed_password,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Define the token expiration time
    TOKEN_EXPIRATION_TIME = timedelta(hours=48)

    # Generate the JWT token using the new function
    token = create_access_token(
        data={"id": new_user.id, "sub": new_user.username, "role": new_user.role},
        expires_delta=TOKEN_EXPIRATION_TIME,
    )

    # Return the token
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, login_data: login_dependency):
    new_user = db.query(DBUsers).filter(DBUsers.username == login_data.username).first()
    is_password_matching = verify_password(
        login_data.password, new_user.hashed_password
    )

    if not new_user or not is_password_matching:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Define the token expiration time
    TOKEN_EXPIRATION_TIME = timedelta(hours=48)

    # Generate the JWT token using the new function
    token = create_access_token(
        data={"id": new_user.id, "sub": new_user.username, "role": new_user.role},
        expires_delta=TOKEN_EXPIRATION_TIME,
    )

    # Return the token
    return {"access_token": token, "token_type": "bearer"}


@router.delete("/remove_user", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(db: db_dependency, login_data: login_dependency):
    user_model = db.query(DBUsers).filter(DBUsers.username == login_data.username).first()
    is_password_matching = verify_password(
        login_data.password, user_model.hashed_password
    )

    if not user_model or not is_password_matching:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Remove the user
    db.delete(user_model)
    db.commit()
