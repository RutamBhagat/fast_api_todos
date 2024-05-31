from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine
from app.routers import auth, todos, admin, users, addresses
from dotenv import load_dotenv

from app import models


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


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
