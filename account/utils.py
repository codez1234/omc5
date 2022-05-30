from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
            # you can send email to multiple person == to=[data['to_email'], "exm@exm.com", .....]

        )
        email.send()


'''

# SMTP configuration
EMAIL_HOST = "smtp.gmail.com"  # config('EMAIL_HOST')
EMAIL_PORT = 587  # config('EMAIL_PORT', default=587, cast=int)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True  # config('EMAIL_USE_TLS', cast=bool)



SECRET_KEY=erklgjlkernmgkernlgkerkmgerg
DEBUG=True
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=


'''
