from fastapi import APIRouter, HTTPException, Path
from models import Todo, User
from starlette import status
from database import db_dependency
from routers.todos import TodoRequest
from .auth import (
    UserVerification,
    raise_admin_authentication_error,
    raise_authentication_error,
    user_dependency,
    bcrypt_context,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    raise_authentication_error(user)

    found_user = db.query(User).filter(User.id == user.get("id")).first()

    return found_user


@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerification,
):
    raise_authentication_error(user)

    found_user = db.query(User).filter(User.id == user.get("id")).first()

    raise_authentication_error(found_user)

    if not bcrypt_context.verify(
        user_verification.password, found_user.hashed_password
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Error on password verification."
        )

    found_user.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(found_user)
    db.commit()
