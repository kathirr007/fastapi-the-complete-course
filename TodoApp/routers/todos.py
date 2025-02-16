from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from models import Todos
from starlette import status
from database import db_dependency

router = APIRouter()

# app.include_router(auth.router)


class TodoRequest(BaseModel):
    title: str = Field(min_length=5)
    description: str = Field(min_length=5, max_length=300)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Write todo title",
                "description": "Short description about the todo",
                "priority": 5,  # greater than 0 and less than 6
                "complete": False,
            }
        }
    }


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    found_todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if found_todo is not None:
        return found_todo

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found.")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def add_todo(db: db_dependency, todo_request: TodoRequest):

    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):

    found_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if found_model is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    found_model.title = todo_request.title
    found_model.description = todo_request.description
    found_model.priority = todo_request.priority
    found_model.complete = todo_request.complete

    db.add(found_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    found_todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if found_todo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
