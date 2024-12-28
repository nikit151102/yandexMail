from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_PORT=587,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_USERNAME="Rebuild-Pro@yandex.ru",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="Rebuild-Pro@yandex.ru",
    MAIL_PASSWORD="eychbqzatnyoncjd",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
