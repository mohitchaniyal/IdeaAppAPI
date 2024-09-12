from fastapi import FastAPI
import models
from database import engine
from routers import ideas,users,auth,likes
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
origins = [
"*"
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_home():
    return {"detail":"Welcome to idea app"}
app.include_router(ideas.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
