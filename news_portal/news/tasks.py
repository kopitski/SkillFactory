from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category, User
from datetime import timedelta, datetime, date


def get_subscribers(Category):
    user_emails = []
    #Получаем id всех подписчиков
    subs_id = Category.objects.all().values_list('subscribers', flat=True)

    #Получаем их эл.почты
    for subs in subs_id:
        user_emails.append(User.objects.filter(id=subs).values_list('email', flat=True).first())
    return user_emails


def notify_weekly():
    week = timedelta(days=7)
    posts = Post.objects.all()
    past_week_posts = []

    finish = datetime.now()
    start = datetime.now() - week
    for post in posts:
        time_delta = date.today() - post.publish_time.date()
        if (time_delta < week):
            past_week_posts.append(post)

    past_week_categories = set()
    for post in past_week_posts:
        past_week_categories.add(Post.objects.filter(title=post).values('post_category'))

    for category in past_week_categories:
        sub_ids = []
        sub_ids.append(Category.objects.filter(postcategory__in=category).values('subscribers'))
        sub_email = []
        sub_name = []

        for sub in sub_ids:
            sub_email.append(User.objects.filter(id=sub).values_list('email', flat=True).first())
            sub_name.append(User.objects.filter(id=sub).values_list('username', flat=True).first())

        post_object = []
        post_object.append(Post.objects.filter(post_category__in=category, publish_time__range=[start, finish]).values_list('title', flat=True))
        post_url = []
        url_base = 'http://127.0.0.1:8000/news/'
        for post in post_object:
            post_id = str(Post.objects.filter(post_category__in=category, publish_time__range=[start, finish]).values_list('id', flat=True))
            post_url = url_base + post_id

        html_content = render_to_string(
            'mail/weekly_update.html',
            {'post': post_object, 'username': sub_name, 'post_url': post_url}
        )
        for i in range(len(sub_ids)):
            #url = '27.0.0.1:8000/news/' + str(post_url[i])
            msg = EmailMultiAlternatives(
                subject=f'Greeting {sub_name}! Your weekly update',
                body=f'{post_object}',
                from_email='Kopitski92@yandex.ru',
                to=[sub_email[i], ],

            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()