from fastapi import FastAPI
from app.database import engine, Base
from app.api import user
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"msg": "启动成功"}