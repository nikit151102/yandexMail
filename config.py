from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_PORT=587,
    MAIL_SERVER="smtp.yandex.com",
    MAIL_USERNAME="nikit50901@yandex.ru",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="nikit50901@yandex.ru",
    MAIL_PASSWORD="oowhswxyretwmodj",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
