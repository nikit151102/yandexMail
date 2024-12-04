from fastapi import FastAPI
from routers import email_router

app = FastAPI()

app.include_router(email_router.router, prefix="/email", tags=["email"])
