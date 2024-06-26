from fastapi import APIRouter, HTTPException, status

from app.auth.hash import verify_password, get_password_hash
from app.db.schema import ChangePasswordBody, UserResponse
from app.db.access_layers import db_users
from app.dependencies import db_dependency, user_dependency


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def read_users_me(user: user_dependency) -> UserResponse:
    return user


# change password of current user
@router.patch("/me/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: db_dependency, user: user_dependency, password_change: ChangePasswordBody
):
    is_password_correct = verify_password(
        password_change.password, user.hashed_password
    )
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect previous password",
        )

    hashed_password = get_password_hash(password_change.new_password)
    user.hashed_password = hashed_password
    await db_users.update_user(db, user)
