import os
from email.message import EmailMessage
import aiosmtplib
from utils.template_engine import render_template

async def send_reset_email(
    to_email: str,
    template: str,
    configTemplate: object,
    subject: str = 'Restablece tu contraseña',
) -> None:
    """
    Envía un correo electrónico para restablecer la contraseña.
    """

    html_content = render_template(template, configTemplate)

    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_FROM", "hello@demomailtrap.com")
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(html_content, subtype="html")

    email_port = os.getenv("EMAIL_PORT")
    hostname = os.getenv("EMAIL_HOST")
    username = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    
    if email_port is None:
        raise ValueError("EMAIL_PORT environment variable is not set")
    await aiosmtplib.send(
        msg,
        hostname=hostname,
        port=int(email_port),
        username=username,
        password=password,
        use_tls=False,
        start_tls=True,
    )