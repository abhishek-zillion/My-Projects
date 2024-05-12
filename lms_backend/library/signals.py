# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    print(f"Received user_logged_in signal for user: {user.username}")
    print(f"Request method: {request.method}")
    print(f"Request path: {request.path}")
    print(f"Sender model: {sender.__name__}")
    user.login_time = timezone.now()
    user.save()
