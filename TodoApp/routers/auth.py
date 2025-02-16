from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from database import db_dependency
from starlette import status
from jose import JWTError, jwt
from models import User


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=5)


SECRET_KEY = "thisMyVeryVerySecretKey"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str, db):
    found_user: User = db.query(User).filter(User.username == username).first()

    if not found_user or not bcrypt_context.verify(
        password, found_user.hashed_password
    ):
        return False
    return found_user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):

    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user."
            )
        return {"username": username, "id": user_id, "user_role": user_role}

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user."
        )


def raise_authentication_error(user: User):
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated."
        )


def raise_admin_authentication_error(user: User):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated as admin."
        )


user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("")
async def auth_user():
    return {"user": "authenticated"}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    created_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(created_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_authentication_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="User not authenticated."
        )
        # return "Authentication failed."

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
