# users/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(email):
    subject = 'Welcome to Our Service'
    message = 'Thank you for signing up!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def log_failed_login_attempt(email):
    logger.warning(f'Failed login attempt for user: {email}')
