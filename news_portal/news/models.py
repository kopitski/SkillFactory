from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    """author_user: связь «один к одному» с встроенной моделью пользователей User
       user_rating: рейтинг автора"""

    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        """Суммарный рейтинг всех статей автора, умножен на 3"""
        art_sum = Post.objects.filter(author=self).aggregate(Sum('_post_rating')).get('_post_rating__sum') * 3

        """Суммарный рейтинг всех комментариев автора"""
        comm_sum = Comment.objects.filter(comment_user_id=self.author_user).aggregate(Sum('_comment_rating'))
        comm_sum = comm_sum.get('_comment_rating__sum')

        """Суммаррный рейтинг всех комментариев к статьям автора"""
        art_comm = Comment.objects.filter(comment_post_id__in=Post.objects.filter(author=self)).aggregate(Sum('_comment_rating'))
        art_comm = art_comm.get('_comment_rating__sum')

        """Общая сумма"""
        self.user_rating = art_sum + comm_sum + art_comm
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    """Категории новостей/статей — темы, которые они отражают"""
    categories = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def subscribe(self):
        pass

    def get_category(self):
        return self.categories

    def __str__(self):
        return self.categories


class Post(models.Model):
    """<author>        связь «один ко многим» с моделью Author;
       <category_type> поле с выбором — «статья» или «новость»;
       <publish_time>  автоматически добавляемая дата и время создания;
       <post_category> связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
       <title>         заголовок статьи/новости;
       <text>          текст статьи/новости;
       <_post_rating>  рейтинг статьи/новости."""

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = "AR"
    CATEGORY_CHOICES = [
        (NEWS, "Новость"),
        (ARTICLE, "Статья")
    ]
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    publish_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField("Category", through="PostCategory")
    title = models.CharField(max_length=64)
    text = models.TextField()
    _post_rating = models.IntegerField(default=0, db_column='post_rating')

    "Методы like и dislike которые увеличивают/уменьшают рейтинг на единицу"
    def like(self):
        self._post_rating += 1
        self.save()

    def dislike(self):
        self._post_rating -= 1
        self.save()

    "Метод preview возвращает предварительный просмотр длиной 124 символов"
    def preview(self):
        if len(str(self.text)) < 124:
            return self.text
        else:
            return self.text[:124] + '...'

    def email_preview(self):
        return f'{self.text[0:50]}...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    """Промежуточная модель для связи «многие ко многим»:
        связь «один ко многим» с моделью Post;
        связь «один ко многим» с моделью Category."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
        Модель будет иметь следующие поля:
        <comment_post>    связь «один ко многим» с моделью Post;
        <comment_user>    связь «один ко многим» со встроенной моделью User
                          (комментарии может оставить любой пользователь, необязательно автор);
        <comment_text>    текст комментария;
        <comment_date>    дата и время создания комментария;
        <_comment_rating> рейтинг комментария."""

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    _comment_rating = models.IntegerField(default=0, db_column='comment_rating')

    "Методы like и dislike которые увеличивают/уменьшают рейтинг на единицу"
    def like(self):
        self._comment_rating += 1
        self.save()

    def dislike(self):
        self._comment_rating -= 1
        self.save()