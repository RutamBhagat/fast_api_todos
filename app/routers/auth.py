from fastapi import APIRouter, HTTPException, status
from app.auth.auth import get_password_hash, verify_password, create_access_token
from app.db.models import DBUsers
from app.db.schema import UserBody
from app.dependencies import db_dependency, login_dependency
from app.db.access_layers import db_users

router = APIRouter(prefix="/auth", tags=["auth"])

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserBody):
    try:
        user_already_exists = await db_users.get_user(
            db, create_user_request.username, create_user_request.email
        )
        if user_already_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists",
            )
    except Exception as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            # This is desired behavior, the user does not exist
            pass
        else:
            raise
    user = await db_users.create_user(db, create_user_request)
    token = create_access_token(
        data={"id": user.id, "sub": user.username, "role": user.role},
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, login_data: login_dependency):
    user = await db_users.get_user(db, login_data.username)
    is_password_matching = verify_password(login_data.password, user.hashed_password)
    if not is_password_matching:
        raise invalid_credentials_exception
    token = create_access_token(
        data={"id": user.id, "sub": user.username, "role": user.role}
    )
    return {"access_token": token, "token_type": "bearer"}


@router.delete("/remove_user", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(db: db_dependency, login_data: login_dependency):
    user = await db_users.get_user(db, login_data.username)
    is_password_matching = verify_password(login_data.password, user.hashed_password)
    if not is_password_matching:
        raise invalid_credentials_exception
    await db_users.delete_user(db, user)
