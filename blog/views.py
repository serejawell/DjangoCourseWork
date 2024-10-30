from blog.services import get_posts_from_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return get_posts_from_cache()

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        '''Добавление дополнительной информации в контекст'''
        context = super().get_context_data(**kwargs)
        context['post'].views += 1  # Увеличиваем количество просмотров
        context['post'].save()  # Сохраняем изменения
        return context

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
