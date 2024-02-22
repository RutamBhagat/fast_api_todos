from models import Users
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from .utils.type_classes import CreateUserRequest
from .utils.utility_funcs import (
    db_dependency,
    login_dependency,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
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
    new_user = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=hashed_password,
        role=create_user_request.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    del new_user.hashed_password
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, login_data: login_dependency):
    user_model = db.query(Users).filter(Users.username == login_data.username).first()
    is_password_matching = verify_password(
        login_data.password, user_model.hashed_password
    )

    if not user_model or not is_password_matching:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Define the token expiration time
    TOKEN_EXPIRATION_TIME = timedelta(hours=48)

    # Generate the JWT token using the new function
    token = create_access_token(
        data={"id": user_model.id, "sub": user_model.username, "role": user_model.role},
        expires_delta=TOKEN_EXPIRATION_TIME,
    )

    # Return the token
    return {"access_token": token, "token_type": "bearer"}


@router.delete("/remove_user", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(db: db_dependency, login_data: login_dependency):
    user_model = db.query(Users).filter(Users.username == login_data.username).first()
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


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
