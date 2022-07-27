import sys
import socket

from datetime import datetime, timedelta, date
from django.utils import timezone

from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст

from .models import Post, PostCategory, CategorySubscribers
from NewsPaper.settings import DEFAULT_FROM_EMAIL  # для почтового ящика по умолчанию
# from .tasks import send_mail_new_post  # Импортируем задачу для асинхронной задачи


@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, action, **kwargs):
    """  С помощью данного метода мы создаем "post_add" который отправляется после добавления одного или нескольких
    объектов. Далее с помощью instance - экземпляр, чье отношение «многие-ко-многим» обновляется, мы можем получить
    все посты всех категорий. С помощью фильтрации получаем категорию на которую подписан пользователь. Формируем
    тему и сообщение с помощью EmailMultiAlternatives, так же получаем список e-mail пользователей для рассылки.
    """
    if action == 'post_add':
        for cat in instance.post_category.all():
            for subscribe in CategorySubscribers.objects.filter(category=cat):

                msg = EmailMultiAlternatives(
                    subject=instance.headline,
                    body=instance.post_text,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[subscribe.subscriber_user.email],
                )

                " Получения ссылки поста в теле письма "
                # тут с помощью импортированной библиотеки sys получаем срез второй символ по индексу в обратном порядке
                port = sys.argv[-2]  # костыльный способ получения http://ip:port
                # current_site = Site.objects.get_current()  # Это нужно для получения корректной ссылке на продакшене

                html_content = render_to_string(
                    'post_create.html',
                    {
                        'posts': instance.post_text,
                        'recipient': subscribe.subscriber_user.email,
                        'category_name': subscribe.category,
                        'subscriber_user': subscribe.subscriber_user,
                        'pk_id': instance.pk,
                        'date': instance.create_date,
                        # 'current_site': current_site.domain,  # на продакшен
                        'port': port,  # это ключ который мы прописываем в шаблоне
                    },
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # print(f'{instance.headline} {instance.post_text}')
                # print('Уведомление отослано подписчику ',
                #       subscribe.subscriber_user, 'на почту',
                #       subscribe.subscriber_user.email, ' на тему ', subscribe.category)


def collect_subscribers(category):
    """ Перебрать всех подписчиков в таблице категорий, извлечь их электронную почту
     и сформировать список получателей электронной почты """
    email_recipients = []
    for user in category.subscribers.all():
        email_recipients.append(user.email)
    # print(f'collect_subscribers func: {email_recipients}')
    return email_recipients


def send_emails(post_object, *args, **kwargs):
    """ Функция подготовки всех постов для передачи любых переменных в шаблон HTML который будет сформирован
    render_to_string и отправлен на почту подписчикам """
    # print(kwargs['template'])
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},  # передаем в шаблон любые переменные
    )
    # print(kwargs['category_object'], )

    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email=DEFAULT_FROM_EMAIL,
        to=kwargs['email_recipients']  # отправляем всем из списка
    )
    print(kwargs)
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)


def week_post_2():
    """ Функция отправки рассылки подписчикам за неделю """
    week = timedelta(days=7)
    posts = Post.objects.all()
    past_week_posts = []
    template = 'weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for post in posts:
        time_delta = date.today() - post.create_date.date()
        if time_delta < week:
            past_week_posts.append(post)

    past_week_categories = set()
    for post in past_week_posts:
        for category in post.post_category.all():
            past_week_categories.add(category)
    # print(f'past_week_categories = {past_week_categories}')

    email_recipients_set = set()
    for category in past_week_categories:
        # print(f'category.subscribers.all = {category.subscribers.all()}')
        # запрос почтового ящика пользователя
        get_user_emails = set(collect_subscribers(category))
        email_recipients_set.update(get_user_emails)
        # print(f'get_user_emails = {get_user_emails}')
    email_recipients = list(email_recipients_set)
    # print(email_recipients)

    for email in email_recipients:
        post_object = []
        categories = set()

        for post in past_week_posts:
            subscription = post.post_category.all().values('subscribers').filter(subscribers__email=email)

            if subscription.exists():
                # print(f'subscription = {subscription}')
                post_object.append(post)
                categories.update(post.post_category.filter(subscribers__email=email))

        # print(f'email = {email}')
        # print(f'post_object = {post_object}')

        category_object = list(categories)

        # print(f'category_object = {category_object}')
        # print(f'set(post.cats.all()) = {set(post.post_category.all())}')

        send_emails(
            post_object,
            category_object=category_object,
            email_subject=email_subject,
            template=template,
            email_recipients=[email, ]
        )
