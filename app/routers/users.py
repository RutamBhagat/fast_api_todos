from fastapi import APIRouter, HTTPException, status

from app.db.schema import ChangePasswordBase
from app.auth.auth import verify_password, get_password_hash
from app.dependencies import db_dependency, user_dependency

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_users_me(user: user_dependency):
    print(user)
    del user.hashed_password
    return user


# change password of current user
@router.patch("/me/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: db_dependency, user: user_dependency, password_change: ChangePasswordBase
):
    is_password_correct = verify_password(
        password_change.password, user.hashed_password
    )
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect previous password",
        )

    hased_password = get_password_hash(password_change.new_password)
    user.hashed_password = hased_password
    db.add(user)
    db.commit()
    db.refresh(user)
