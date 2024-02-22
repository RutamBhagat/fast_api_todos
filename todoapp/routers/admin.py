from fastapi import APIRouter, HTTPException, status
from .utils.utility_funcs import user_dependency, db_dependency
from models import Todo

router = APIRouter()


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return db.query(Todo).all()
