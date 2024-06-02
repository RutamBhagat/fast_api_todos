from typing import Optional
from sqlalchemy.orm.session import Session
from app.db.hash import get_password_hash
from app.db.models import DBUsers
from app.db.schema import UserBody
from fastapi import HTTPException, status

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)


# find user by username or email
async def get_user(
    db: Session, username: Optional[str] = None, email: Optional[str] = None
) -> DBUsers:
    if username is not None:
        user = db.query(DBUsers).filter(DBUsers.username == username).first()
        if user is None:
            raise user_not_found
        return user
    elif email is not None:
        user = db.query(DBUsers).filter(DBUsers.email == email).first()
        if user is None:
            raise user_not_found
        return user
    else:
        raise user_not_found


# create a new user
async def create_user(db: Session, user: UserBody) -> DBUsers:
    hashed_password = get_password_hash(user.password)
    del user.password
    user = DBUsers(**user.model_dump(), hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# delete a user
async def delete_user(db: Session, user: DBUsers) -> None:
    db.delete(user)
    db.commit()


# update a user
async def update_user(db: Session, user: DBUsers):
    db.add(user)
    db.commit()
    db.refresh(user)
