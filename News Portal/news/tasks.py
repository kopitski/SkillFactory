from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category, User
from datetime import timedelta, datetime
from django.shortcuts import redirect
from celery import shared_task


@shared_task
def new_post_mail(instance):
    last_post = instance
    last_post_categories = last_post.post_category.all()
    last_post_categories_id = [category.id for category in last_post_categories]
    category = Category.objects.filter(id__in=last_post_categories_id).values_list('categories', flat=True).first()

    users = []
    for category_id in last_post_categories_id:
        subscribers = Category.objects.get(pk=category_id).subscribers.all()
        users.extend(subscribers)
    users = list(set(users))

    cat = f'{category}'
    post_url = 'http://127.0.0.1:8000/news/' + str(last_post.id)

    for i in range(len(users)):
        username = users[i].username
        html_content = render_to_string(
            'mail/new_post.html',
            {'categories': cat,
             'post_url': post_url,
             'title': last_post.title,
             'text': last_post.text,
             'username': username},
        )

        msg = EmailMultiAlternatives(
            subject=f'Hello {username}! New post has been posted in your favorite category! {cat}',
            body=f'{last_post.title}\n{last_post.text}',
            from_email='Kopitski92@yandex.ru',
            to=[f'{users[i].email}'],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

    return redirect('news_list')


@shared_task
def notify_weekly():
    """Получаем список подписчиков"""
    subs = []
    for i in Category.objects.all().values_list('subscribers', flat=True).distinct():
        subs.append(i)
        subs = [i for i in subs if i is not None]

    week = timedelta(days=7)
    finish = datetime.now()
    start = datetime.now() - week
    """Определяем категории и статьи по каждому подписчику и отправляем"""
    for sub in subs:
        sub_cat = Category.objects.filter(subscribers=sub).values_list('id', flat=True)
        categories = Category.objects.filter(id__in=sub_cat).values_list('categories', flat=True)

        for i in sub_cat:
            posts = Post.objects.filter(post_category__in=sub_cat, publish_time__range=[start, finish])

        username = User.objects.get(id=sub)
        email = username.email
        cat = ",".join(categories)

        html_content = render_to_string(
            'mail/weekly_update.html',
            {'categories': categories,
             'posts': posts,
             'username': username},
        )
        """Яндекс отправляет почту на gmail, но иногда проект вылетает с ошибкой спам"""
        msg = EmailMultiAlternatives(
            subject=f'Hello {username}! Your weekly update for your favorite category: {cat}',
            body="",
            from_email='Kopitski92@yandex.ru',
            to=[email, ],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    #return redirect('news_list')