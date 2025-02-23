from fastapi import HTTPException, UploadFile
from fastapi_mail import FastMail, MessageSchema
import base64
from models import EmailRecord
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select



async def encode_file_to_base64(file: UploadFile):
    """Функция для кодирования файла в base64"""
    file_content = await file.read()
    return base64.b64encode(file_content).decode('utf-8')



def get_mime_type(file_extension: str) -> str:
    """Функция для определения MIME-типа файла по расширению"""
    if file_extension == 'png':
        return 'image/png'
    elif file_extension in ['jpg', 'jpeg']:
        return 'image/jpeg'
    elif file_extension == 'gif':
        return 'image/gif'
    else:
        return 'application/octet-stream'



async def get_emails_from_db(db: AsyncSession):
    """Функция для извлечения всех email из базы данных"""
    try:
        result = await db.execute(select(EmailRecord.email))
        return result.scalars().all() 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching emails from DB: {str(e)}")



async def send_email_with_attachment(fm: FastMail, subject: str, message: str, file_base64: str, mime_type: str, email: str):
    """Функция для отправки email с вложением"""
    body = f"""
        <img src="data:{mime_type};base64,{file_base64}" alt="Image">
        <p>{subject}</p>
        <p>{message}</p>
    """
    email_message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html",
    )
    try:
        await fm.send_message(email_message)
        return True
    except Exception as e:
        return str(e)



async def send_email_with_attachment_from_txt(fm: FastMail, subject: str, message: str, mime_type: str, email: str):
    """Функция для отправки email с вложением"""
    body = f"""
        <p>{subject}</p>
        <p>{message}</p>
    """
    email_message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html",
    )
    try:
        await fm.send_message(email_message)
        return True
    except Exception as e:
        return str(e)

