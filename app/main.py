import logging
from fastapi import FastAPI
from .routers import books, users, reviews, recommendations
from .database import engine, Base

logging.basicConfig(level=logging.DEBUG)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(books.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(recommendations.router)



@app.get("/")
def read_root():
    return {"message": "Welcome to Book Review Service! Go to /docs for API documentation"}
