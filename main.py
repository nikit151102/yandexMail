from fastapi import FastAPI
from routers import email_router
from routers import crud_emails, subscribe
from database.database_app import create_db_if_not_exists, create_tables 
import subprocess

def run_migrations():
    """Выполнить миграции перед запуском приложения."""
    try:
        subprocess.run(
            ["alembic", "upgrade", "head"], 
            check=True,
            capture_output=True,
            text=True
        )
        print("Миграции успешно выполнены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении миграций: {e.stderr}")


create_db_if_not_exists()
create_tables()

run_migrations()



app = FastAPI()

app.include_router(email_router.router, prefix="/email", tags=["emailing"])
app.include_router(crud_emails.router, prefix="/emails", tags=["email-crud"])
app.include_router(subscribe.router, prefix="/subscribe", tags=["email subscribe"])
