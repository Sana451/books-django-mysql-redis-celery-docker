from celery import shared_task
from django.conf import settings
from django.core.signing import Signer
from django.template.loader import render_to_string
from .models import AdvUser

signer = Signer()


@shared_task
def send_activation_notification(username):
    user = AdvUser.objects.get(username=username)
    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)
    return subject
