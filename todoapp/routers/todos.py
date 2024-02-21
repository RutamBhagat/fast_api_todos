from typing import Annotated
from fastapi import Depends, HTTPException, Path, status, APIRouter
from pydantic import BaseModel, Field
from models import Todo
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# this is just a type hint
db_dependency = Annotated[Session, Depends(get_db)]


class Todo_Request(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., ge=0, le=5)
    completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Now to do chores",
                "description": "Wash the clothes and hang them to dry",
                "priority": 3,
                "completed": False,
            }
        }


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todo).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_one_todo(db: db_dependency, todo_id: int = Path(..., ge=1)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo_model


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(db: db_dependency, new_todo: Todo_Request):
    todo = Todo(**new_todo.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)


# Todo put request
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, updated_todo: Todo_Request, todo_id: int = Path(..., ge=1)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.priority = updated_todo.priority
    todo.completed = updated_todo.completed
    db.commit()
    db.refresh(todo)


# Todo delete request
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(..., ge=1)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
