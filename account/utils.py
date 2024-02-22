from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data["to_email"]],
        )
        print("sdadadadadadadsadadas")
        print(data["subject"])
        print(data["body"])
        print(data["to_email"])
        print(os.environ.get("EMAIL_FROM"))

        email.send()
