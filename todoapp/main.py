from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos
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
