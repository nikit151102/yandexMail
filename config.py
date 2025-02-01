from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_PORT=587,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_USERNAME="support@rebuildpro.ru",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="support@rebuildpro.ru",
    MAIL_PASSWORD="yohqnuvomfsrytmk",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
