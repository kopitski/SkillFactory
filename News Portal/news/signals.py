from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def send_mail_to_subs(sender, instance, **kwargs):
    last_post = Post.objects.last()
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