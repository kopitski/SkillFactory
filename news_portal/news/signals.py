from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory, User


@receiver(post_save, sender=Post)
def send_mail_to_subs(sender, instance, created, **kwargs):
    new_post_id = PostCategory.objects.order_by('-post_id')[0].post_id
    cat = PostCategory.objects.filter(post_id=new_post_id).values('category_id')
    cat_name = Category.objects.filter(id__in=cat).values_list('categories', flat=True).first()
    subs_id = Category.objects.filter(id__in=cat).values_list('subscribers', flat=True).distinct()
    test = len(subs_id)

    text = Post.objects.get(pk=new_post_id).text
    title = Post.objects.get(pk=new_post_id).title
    post_url = 'http://127.0.0.1:8000/news/' + str(new_post_id)

    #Получаем список всех username подписчиков
    subs_username = []
    for i in range(test):
        subs_username.append(User.objects.filter(id=subs_id[i]).values_list('username', flat=True).first())

    # Получаем список всех email подписчиков
    sub_email = []
    for i in range(test):
        sub_email.append(User.objects.filter(id=subs_id[i]).values_list('email', flat=True).first())

    html_content = render_to_string(
        'mail/new_post.html',
        {'categories': cat_name, 'username': subs_username, 'post_url': post_url, 'title': title, 'text': text},
    )
    for i in range(test):
        msg = EmailMultiAlternatives(
            subject=f'Привет {subs_username[i]}! Новая статья в твоём любимом разделе! {cat_name}',
            body=f'{title}\n{text}',
            from_email='Kopitski92@yandex.ru',
            to=[sub_email[i]],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

    return redirect('news_list')