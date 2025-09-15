from django.dispatch import Signal,receiver
from django.core.mail import send_mail
from django.conf import settings

manual_signal = Signal()

@receiver(manual_signal)
def user_logged(sender, user, **kwargs):

    subject = "Login Alert"
    message = f"Hi {user.username},\nyou have just logged into your account"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently = False,
    )