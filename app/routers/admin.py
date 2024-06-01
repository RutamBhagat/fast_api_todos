from fastapi import APIRouter, HTTPException, Path, status
from app.dependencies import user_dependency, db_dependency
from app.db.models import DBTodo

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return db.query(DBTodo).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(..., ge=1)
):
    if user is None or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DBTodo not found",
        )
    db.delete(todo)
    db.commit()
    return {"message": f"DBTodo item with ID {todo_id} has been successfully deleted."}
