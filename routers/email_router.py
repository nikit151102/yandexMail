from fastapi import APIRouter, HTTPException, UploadFile, File, Depends,Form, WebSocket, WebSocketDisconnect
from fastapi_mail import FastMail, MessageSchema
from config import conf
from modelsDTO.email_models import LinkRequest, TextMessageRequest
from fastapi_mail import ConnectionConfig
import crudEmail
import defs_send_emails
from pydantic import BaseModel, EmailStr
import schemas
from fastapi import Depends
from database.database_app import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Union
import random
import asyncio


router = APIRouter()


@router.post("/send-registration-confirmation/")
async def send_registration_confirmation(mail_request: LinkRequest):
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
async def send_password_reset(mail_request: LinkRequest):
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
async def send_custom_message(request: TextMessageRequest):
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





@router.post("/send-emailing-messages/")
async def send_bulk_message(
    subject: str = Form(...),
    message: str = Form(...),
    file: Union[UploadFile, None] = File(None),
    min_interval: int = Form(...),
    max_interval: int = Form(...),
    emailsPerPage: int = Form(...),
    db: AsyncSession = Depends(get_session),
):
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
