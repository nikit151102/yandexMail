from fastapi import FastAPI
from routers import email_router
from routers import crud_emails

app = FastAPI()

app.include_router(email_router.router, prefix="/email", tags=["emailing"])
app.include_router(crud_emails.router, prefix="/emails", tags=["email-crud"])
