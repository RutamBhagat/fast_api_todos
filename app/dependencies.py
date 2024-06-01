from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.db.database import get_db
from app.auth.auth import oauth2_scheme


login_dependency = Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]
