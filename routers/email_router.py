from fastapi import APIRouter, HTTPException
from fastapi_mail import FastMail, MessageSchema
from config import conf
from models.email_models import LinkRequest, TextMessageRequest
from fastapi_mail import ConnectionConfig

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
        subject="Сброс пароля для Виткон сервис",
        recipients=[mail_request.email],
        body=f"""
        <p>Здравствуйте,</p>
        <p>Чтобы изменить ваш пароль, перейдите по следующей ссылке:</p>
        <p><a href="{mail_request.link}">Сбросить пароль</a></p>
        <p>С уважением, </p>
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
        <p>С уважением, </p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"status": "Custom message email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
