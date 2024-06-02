from fastapi import APIRouter, HTTPException, Path, status
from app.db.schema import TodoBody, TodoResponse
from app.db.access_layers import db_todos
from app.dependencies import db_dependency, user_dependency


router = APIRouter(prefix="/todos", tags=["todos"])
todo_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="DBTodo not found for given user",
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
async def read_all(db: db_dependency, user: user_dependency):
    return await db_todos.get_todos(db, user)


@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read_one_todo(
    db: db_dependency, user: user_dependency, todo_id: int = Path(..., ge=1)
):
    return await db_todos.get_todo(db, user, todo_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
async def create_new_todo(db: db_dependency, user: user_dependency, new_todo: TodoBody):
    return await db_todos.create_todo(db, user, new_todo)


# DBTodo put request
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    user: user_dependency,
    updated_todo: TodoBody,
    todo_id: int = Path(..., ge=1),
):
    await db_todos.update_todo(db, user, updated_todo, todo_id)


# DBTodo delete request
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: db_dependency, user: user_dependency, todo_id: int = Path(..., ge=1)
):
    await db_todos.delete_todo(db, user, todo_id)
