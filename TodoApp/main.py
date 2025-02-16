from fastapi import FastAPI

import models
from routers import admin, auth, todos, users
from database import db_engine

app = FastAPI()

models.Base.metadata.create_all(bind=db_engine)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
