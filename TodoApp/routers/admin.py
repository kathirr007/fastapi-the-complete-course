from fastapi import APIRouter, HTTPException, Path
from models import Todo, User
from starlette import status
from database import db_dependency
from routers.todos import TodoRequest
from .auth import (
    raise_admin_authentication_error,
    user_dependency,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    raise_admin_authentication_error(user)

    return db.query(Todo).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    raise_admin_authentication_error(user)

    found_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if found_todo is not None:
        return found_todo

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found.")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def add_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    raise_admin_authentication_error(user)

    todo_model: Todo = Todo(**todo_request.model_dump())

    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    raise_admin_authentication_error(user)

    found_model = db.query(Todo).filter(Todo.id == todo_id).first()

    if found_model is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    found_model.title = todo_request.title
    found_model.description = todo_request.description
    found_model.priority = todo_request.priority
    found_model.complete = todo_request.complete

    db.add(found_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):

    raise_admin_authentication_error(user)

    found_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if found_todo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency, db: db_dependency):
    raise_admin_authentication_error(user)

    return db.query(User).all()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)
):

    raise_admin_authentication_error(user)

    if user.get("id") == user_id:
        raise HTTPException(
            status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User is not allowed delete his own account.",
        )

    found_user = db.query(User).filter(User.id == user_id).first()

    if found_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found.")

    db.query(User).filter(User.id == user_id).delete()
    db.commit()
