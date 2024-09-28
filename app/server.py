from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.db import models
from app.db.database import engine
from app.routers import auth, todos, admin, users, addresses


load_dotenv()

app = FastAPI()


# Run migrations on startup
@app.on_event("startup")
async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


# Connect to the database
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(addresses.router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
