from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users, addresses
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    todos.router,
    prefix="/todos",
    tags=["todos"],
)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
)
app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
app.include_router(
    addresses.router,
    prefix="/addresses",
    tags=["addresses"],
)
