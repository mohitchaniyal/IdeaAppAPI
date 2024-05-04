from fastapi import FastAPI
import models
from database import engine
from routers import ideas,users,auth,likes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ideas.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)


