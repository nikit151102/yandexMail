from fastapi import APIRouter, HTTPException, UploadFile, File, Depends,Form, WebSocket, WebSocketDisconnect
from fastapi_mail import FastMail, MessageSchema
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import conf
from modelsDTO.email_models import LinkRequest, TextMessageRequest, TextWithIdRequest
from fastapi_mail import ConnectionConfig
import crudEmail
import defs_send_emails
from pydantic import BaseModel, EmailStr
import schemas
from database.database_app import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Union
import random
import asyncio
from services.security_service import verify_credentials
from services.templates_service import get_promo_template_zero_prices


router = APIRouter()
security = HTTPBasic()


@router.post("/send-registration-confirmation/")
async def send_registration_confirmation(
    mail_request: LinkRequest,
    credentials: HTTPBasicCredentials = Depends(security)
):    
    verify_credentials(credentials)
    print("Request authorized!")

    message = MessageSchema(
        subject="Подтверждение регистрации",
        recipients=[mail_request.email],
        body=f"""
        <p>Для завершения регистрации перейдите по следующей ссылке:</p>
        <p><a href="{mail_request.link}">Подтвердить регистрацию</a></p>
        """,
        subtype="html"
    )
    
    print(message)

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"status": "Registration confirmation email sent"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


@router.post("/send-password-reset/")
async def send_password_reset(
    mail_request: LinkRequest,
    credentials: HTTPBasicCredentials = Depends(security)
):    
    verify_credentials(credentials)
    print("Request authorized!")

    message = MessageSchema(
        subject="Сброс пароля на сервисе rebuildpro.ru",
        recipients=[mail_request.email],
        body=f"""
        <p>Здравствуйте,</p>
        <p>Чтобы изменить ваш пароль, перейдите по следующей ссылке:</p>
        <p><a href="{mail_request.link}">Сбросить пароль</a></p>
        <p>С уважением, rebuildpro </p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"status": "Password reset email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")




@router.post("/send-custom-message/")
async def send_custom_message(
    request: TextMessageRequest,
    credentials: HTTPBasicCredentials = Depends(security)
):    
    verify_credentials(credentials)
    print("Request authorized!")

    message = MessageSchema(
        subject=request.subject,
        recipients=[request.email],
        body=f"""
        <p>Здравствуйте,</p>
        <p>{request.message}</p>
        <p>С уважением, rebuildpro</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"status": "Custom message email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

@router.post("/send-test-message/")
async def send_test_message(
    request: TextWithIdRequest,
    credentials: HTTPBasicCredentials = Depends(security)
):    
    verify_credentials(credentials)
    print("Request authorized!")

    _subj, _body = get_promo_template_zero_prices(request.id)

    message = MessageSchema(
        subject=_subj,
        recipients=[request.email],
        body=_body,
        subtype="html"
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"status": "Custom message email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

@router.post("/send-only-subs-emailing-messages/")
async def send_only_subs_bulk_message(
    # subject: str = Form(...),
    # message: str = Form(...),
    # file: Union[UploadFile, None] = File(None),
    min_interval: int = Form(...),
    max_interval: int = Form(...),
    emailsPerPage: int = Form(...),
    db: AsyncSession = Depends(get_session),
    
    credentials: HTTPBasicCredentials = Depends(security)
):
    '''Отправка промо-сообщений только подписанным почтам'''
    verify_credentials(credentials)
    print("Request authorized!")
    try:
        emails = await defs_send_emails.get_subs_only_emails_from_db(db, True)

        if not emails:
            raise HTTPException(status_code=404, detail="No emails found in the database")

        await db.close()

        fm = FastMail(conf)
        errors = []
        
        email_batches = [emails[i:i + emailsPerPage] for i in range(0, len(emails), emailsPerPage)]

        for batch in email_batches:
            for email in batch:
                # Получить Предмет и Тело письма по шаблону
                _subj, _body = get_promo_template_zero_prices(email.id)

                result = await defs_send_emails.send_email_with_attachment(
                    fm, _subj, _body, None, None, email.email
                )
                if result is not True:
                    errors.append({"email": email, "error": result})

            random_interval = random.randint(min_interval, max_interval)
            print('random_interval', random_interval)
            await asyncio.sleep(random_interval) 

        if errors:
            return {"status": "Partially completed", "errors": errors}

        return {"status": "Emails sent successfully"}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending emails: {str(e)}")


@router.post("/send-emailing-messages/")
async def send_bulk_message(
    subject: str = Form(...),
    message: str = Form(...),
    file: Union[UploadFile, None] = File(None),
    min_interval: int = Form(...),
    max_interval: int = Form(...),
    emailsPerPage: int = Form(...),
    db: AsyncSession = Depends(get_session),
    
    credentials: HTTPBasicCredentials = Depends(security)
):
    verify_credentials(credentials)
    print("Request authorized!")
    try:
        if file:
            file_base64 = await defs_send_emails.encode_file_to_base64(file)
            file_extension = file.filename.split('.')[-1].lower()
            mime_type = defs_send_emails.get_mime_type(file_extension)
        else:
            file_base64 = None
            mime_type = None

        emails = await defs_send_emails.get_emails_from_db(db)

        if not emails:
            raise HTTPException(status_code=404, detail="No emails found in the database")

        await db.close()

        fm = FastMail(conf)
        errors = []

      
        email_batches = [emails[i:i + emailsPerPage] for i in range(0, len(emails), emailsPerPage)]

        for batch in email_batches:
            for email in batch:
                result = await defs_send_emails.send_email_with_attachment(
                    fm, subject, message, file_base64, mime_type, email
                )
                if result is not True:
                    errors.append({"email": email, "error": result})

            random_interval = random.randint(min_interval, max_interval)
            print('random_interval', random_interval)
            await asyncio.sleep(random_interval) 

        if errors:
            return {"status": "Partially completed", "errors": errors}

        return {"status": "Emails sent successfully"}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending emails: {str(e)}")



import logging
import random
import asyncio
from fastapi import BackgroundTasks, Form, File, UploadFile, HTTPException

logger = logging.getLogger("email_sender")
logger.setLevel(logging.DEBUG)  

# Обработчик для записи в файл
file_handler = logging.FileHandler("email_sending.log", encoding="utf-8")
file_handler.setLevel(logging.INFO) 
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG) 
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

async def process_bulk_emails(subject, message, emails, min_interval, max_interval, emailsPerPage):
    """Фоновая задача для отправки email."""
    fm = FastMail(conf)
    errors = []
    total_sent = 0

    email_batches = [emails[i:i + emailsPerPage] for i in range(0, len(emails), emailsPerPage)]

    for batch in email_batches:
        batch_sent = 0
        batch_errors = []
        for email in batch:
            result = await defs_send_emails.send_email_with_attachment_from_txt(
                fm, subject, message, None, email
            )
            if result is True:
                batch_sent += 1
            else:
                batch_errors.append({"email": email, "error": result})

        total_sent += batch_sent
        errors.extend(batch_errors)

        logger.info(f"Отправлена пачка: {len(batch)} писем, Успешно: {batch_sent}, Ошибки: {len(batch_errors)}")
        if batch_errors:
            logger.error(f"Ошибки при отправке: {batch_errors}")

        random_interval = random.randint(min_interval, max_interval)
        logger.debug(f"Случайный интервал перед следующей пачкой: {random_interval}")
        await asyncio.sleep(random_interval)

    logger.info(f"Всего обработано писем: {len(emails)}, Успешно отправлено: {total_sent}, Ошибок: {len(errors)}")


@router.post("/send-emailing-messages-from-txt/")
async def send_bulk_message_from_txt(
    background_tasks: BackgroundTasks,
    subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(...),
    min_interval: int = Form(...),
    max_interval: int = Form(...),
    emailsPerPage: int = Form(...)
):
    try:
        if not file.filename.endswith(".txt"):
            raise HTTPException(status_code=400, detail="Неверный формат файла. Разрешены только .txt файлы")

        file_content = await file.read()
        emails = file_content.decode("utf-8").splitlines()
        emails = [email.strip() for email in emails if email.strip()]

        if not emails:
            raise HTTPException(status_code=400, detail="В файле нет корректных email-адресов")

        background_tasks.add_task(process_bulk_emails, subject, message, emails, min_interval, max_interval, emailsPerPage)

        logger.info("Фоновая отправка email запущена")
        return {"status": "Фоновая отправка email запущена"}

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ошибка при отправке писем: {str(e)}")