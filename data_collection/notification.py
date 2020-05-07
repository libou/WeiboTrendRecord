"""
Error Notification
"""
import logging
import smtplib
from email.mime.text import MIMEText


class Notification(object):
    _instance = None

    def __new__(cls, sender, pw, receiver):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Notification, cls).__new__(cls)
            cls._instance._sender = sender
            cls._instance._pw = pw
            cls._instance._receiver = receiver
        return cls._instance

    def notification(self, content):
        mail_host = "smtp.163.com"

        # Email Notification
        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = self._sender
        message['To'] = self._receiver
        message['Subject'] = "WeiboTrendRecord Notification"

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.login(self._sender, self._pw)
            smtpObj.sendmail(self._sender, self._receiver, message.as_string())
            print("邮件发送成功")
            logging.info("Notification sended successfully")
        except smtplib.SMTPException as e:
            print(e)
            logging.error("Error: Sending Notification - {}".format(e))
