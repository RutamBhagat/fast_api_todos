from fastapi import APIRouter, HTTPException, Path, status
from app.dependencies import user_dependency, db_dependency
from app.db.models import DBTodo
from app.db.access_layers import db_todos

router = APIRouter(prefix="/admin", tags=["admin"])

access_denied = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access Denied",
)


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.role != "admin":
        raise access_denied
    return await db_todos.get_all_todos(db)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(..., ge=1)
):
    if user is None or user.role != "admin":
        raise access_denied
    await db_todos.delete_todo_from_db(db, todo_id)
