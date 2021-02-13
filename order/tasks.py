from celery import shared_task, Celery
from django.core.mail import send_mail
from .models import Order
import os

celery = Celery('tasks', broker='amqp://guest@localhost//')
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "myshop.settings"


@shared_task
def order_created(order_id):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
    Your order id is {}.'.format(order.first_name,
                                 order.id)
    mail_sent = send_mail(subject, message, 'your_mail', [order.email])
    return mail_sent