from app.models import DBTodo
from fastapi import APIRouter, HTTPException, Path, status
from app.schema import Todo_Request
from app.dependencies import db_dependency, user_dependency


router = APIRouter(prefix="/todos", tags=["todos"])
todo_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="DBTodo not found for given user",
)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    todos = db.query(DBTodo).filter(DBTodo.owner_id == user.id).all()
    return todos


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_one_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(..., ge=1)
):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.owner_id == user.id).first()
    if todo is None:
        raise todo_not_found
    return todo


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    user: user_dependency, db: db_dependency, new_todo: Todo_Request
):
    todo = DBTodo(**new_todo.model_dump(), owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)


# DBTodo put request
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    updated_todo: Todo_Request,
    todo_id: int = Path(..., ge=1),
):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.owner_id == user.id).first()
    if todo is None:
        raise todo_not_found
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.priority = updated_todo.priority
    todo.completed = updated_todo.completed
    db.commit()
    db.refresh(todo)


# DBTodo delete request
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(..., ge=1)
):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.owner_id == user.id).first()
    if todo is None:
        raise todo_not_found
    db.delete(todo)
    db.commit()
