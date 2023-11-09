from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import datetime

from celery import shared_task
from .models import Response, Post


def email_sender(subject, from_email, recipient_list, html_content):
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',  # это то же, что и message
        from_email=from_email,
        to=recipient_list,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@shared_task
def response_create_notify(response_text, response_author, response_post, **kwargs):
    response = Response.objects.filter(response_text=response_text,
                        response_author=User.objects.get(id=response_author)).\
                        order_by('-response_creation_time').first()

    html_content = render_to_string(
        'email_notification.html',
        {
            'text': response.response_text[:50],
            'link': f'{settings.SITE_URL}/posts/search'

        }
    )
    post_author = Post.objects.get(id=response_post).post_author
    send_email = post_author.email

    if send_email is not None:
        email_sender(subject='Новый отклик на ваше объявление',
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         recipient_list=[send_email],
                         html_content=html_content)


@shared_task
def response_accepter(response_id, **kwargs):
    response = Response.objects.get(id=response_id)

    html_content = render_to_string(
        'email_accept.html',
        {
            'text': response.response_text[:50],
        }
    )

    send_email = response.response_author.email

    if send_email is not None:
        email_sender(subject='Новый отклик на ваше объявление',
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         recipient_list=[send_email],
                         html_content=html_content)


@shared_task
def weekly_notificator():
    period_end = timezone.now()
    period_start = period_end - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_creation_time__gte=period_start)
    subscribers_email = User.objects.values_list('email', flat=True)

    for email in subscribers_email:
        html_content = render_to_string(
                'weekly_notification.html',
                {
                'posts': posts,
                'SITE_URL': settings.SITE_URL
                }
            )
        email_sender(subject='Еженедельная рассылка',
                     from_email=settings.DEFAULT_FROM_EMAIL,
                     recipient_list=[email],
                     html_content=html_content)
