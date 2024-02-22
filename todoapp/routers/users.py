from fastapi import APIRouter, HTTPException, status
from .utils.utility_funcs import (
    db_dependency,
    user_dependency,
    verify_password,
    get_password_hash,
)

router = APIRouter()


@router.get("/me")
async def read_users_me(user: user_dependency):
    print(user)
    del user.hashed_password
    return user


# change password of current user
@router.patch("/me/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: db_dependency,
    user: user_dependency,
    password: str = None,
    new_password: str = None,
):
    is_password_correct = verify_password(password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect previous password",
        )

    hased_password = get_password_hash(new_password)
    user.hashed_password = hased_password
    db.commit()
    db.refresh(user)
