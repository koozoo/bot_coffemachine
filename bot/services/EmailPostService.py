import asyncio
import time

from bot.services.IPostService import IPostService
from bot.misc.env import Stuff, Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class EmailSendlerService(IPostService):
    __slots__ = ["obj", "text", "method", "subject"]

    def __init__(self, obj, text, subject=f"Заявка на обратную связь из телеграм", method="none"):
        super().__init__(obj, text, method)
        self.subject = subject

    async def send_for_user(self):
        pass

    async def send_for_stuff(self):
        for admin in Stuff.ADMINS_EMAIL:
            msg = MIMEMultipart()
            msg['From'] = Email.EMAIL_LOGIN
            msg['To'] = admin
            msg['Subject'] = self.subject
            msg.attach(
                MIMEText(self.text, 'plain')
            )
            await self.send_email(msg)
            await asyncio.sleep(5)

    async def send_email(self, msg):
        server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        server.ehlo(Email.EMAIL_LOGIN)
        server.login(Email.EMAIL_LOGIN, Email.EMAIL_PWD)
        server.auth_plain()
        server.send_message(msg)
        server.quit()

    async def set_email_attr(self, subject, text):
        self.subject = subject
        self.text = text