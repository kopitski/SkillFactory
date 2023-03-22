from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect


from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm, UserForm



class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'
    # Поле, которое будет использоваться для сортировки объектов
    queryset = Post.objects.order_by('id')
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post.html'
    paginate_by = 2


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other'] = Post.objects.all()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# Добавляем новое представление для создания новостей
class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            if 'news/article' in self.request.path:
                post.category_type = 'AR'
            else:
                post.category_type = 'NW'
            post.author = Author.objects.get_or_create(author_user_id=user)[0]
            post.save()
            return self.form_valid(form)
        return redirect('news:news')


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news:index')
    permission_required = ('news.change_post',)
    permission_denied_message = "Доступ закрыт"

    """Проверяем, совпадает ли id пользователя с id автора, если да, 
    то предоставляем право редактирования новостей/статей"""
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) \
            if self.get_object().author_id == request.user.id else HttpResponse(status=403)

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news/article' in self.request.path:
            post.category_type = 'AR'
        else:
            post.category_type = 'NW'

        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post',)
    permission_denied_message = "Доступ закрыт"

    """Проверяем, совпадает ли id пользователя с id автора, если да, 
    то предоставляем право удаления новостей/статей"""
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) \
            if self.get_object().id == request.user.id else HttpResponse(status=403)