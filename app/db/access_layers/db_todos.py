from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.db.models import DBTodo
from app.db.schema import TodoBody, UserBody

todo_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Todo not found for given user",
)


# ADMIN: read all todos from the database
async def get_all_todos(db: Session) -> list[DBTodo]:
    return db.query(DBTodo).all()


# ADMIN: read one todo from the database
async def get_todo_from_db(db: Session, todo_id: int) -> DBTodo:
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if todo is None:
        raise todo_not_found
    return todo


# ADMIN: delete a todo from the database
async def delete_todo_from_db(db: Session, todo_id: int) -> None:
    todo = get_todo_from_db(db, todo_id)
    db.delete(todo)
    db.commit()


# read all todos for a user
async def get_todos(db: Session, request: UserBody) -> list[DBTodo]:
    return db.query(DBTodo).filter(DBTodo.owner_id == request.id).all()


# read a single todo for a user
async def get_todo(db: Session, request: UserBody, todo_id: int) -> DBTodo:
    todo = (
        db.query(DBTodo)
        .filter(DBTodo.id == todo_id, DBTodo.owner_id == request.id)
        .first()
    )
    if todo is None:
        raise todo_not_found
    return todo


# create a new todo
async def create_todo(db: Session, request: UserBody, todo: TodoBody) -> DBTodo:
    todo = DBTodo(**todo.model_dump(), owner_id=request.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# update a todo
async def update_todo(
    db: Session, request: UserBody, todo: TodoBody, todo_id: int
) -> DBTodo:
    todo = await get_todo(
        db, request, todo_id
    )  # This is where you reuse the above function
    todo.update(todo.model_dump())
    db.commit()
    db.refresh(todo)
    return todo


# delete a todo
async def delete_todo(db: Session, request: UserBody, todo_id: int) -> None:
    todo = await get_todo(
        db, request, todo_id
    )  # This is where you reuse the above function
    db.delete(todo)
    db.commit()
