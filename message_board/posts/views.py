from django.shortcuts import redirect
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.translation import gettext
from django.urls import reverse_lazy
from django.utils import timezone
import datetime

from .forms import *
from .filters import ResponseFilter
from .tasks import response_create_notify, response_accepter


class PostList(ListView):
    model = Post
    ordering = 'post_creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_author = self.request.user
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostEditForm
    model = Post
    template_name = 'update_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.post_author != self.request.user:
            return HttpResponseForbidden(
                gettext(
                "Только автор статьи может её редактировать"
                )
            )
        else:
            return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete_form.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        post = self.get_object()
        if post.post_author != self.request.user:
            return HttpResponseForbidden(
                gettext(
                "Только автор статьи может её удалить"
                )
            )
        else:
            return super().form_valid(form)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        connected_responses = (
            Response.objects.filter(response_post=self.get_object()))
        number_of_responses = connected_responses.count()
        data['responses'] = connected_responses
        data['no_of_responses'] = number_of_responses
        data['response_form'] = ResponseForm()
        return data

    def post(self, request, *args, **kwargs):
        response_form = ResponseForm(self.request.POST)
        if response_form.is_valid():
            response_text = response_form.cleaned_data['response_text']
        new_response = Response(response_text=response_text,
                                response_author=self.request.user,
                                response_post=self.get_object())
        new_response.save()
        (response_create_notify.apply_async(
            [
                response_text,
                self.request.user.id,
                self.get_object().id
            ],
            eta=timezone.now() + datetime.timedelta(seconds=10)
                                           )
        )
        return redirect(self.request.path_info)


class SearchResponse(LoginRequiredMixin, ListView):
    model = Response
    ordering = 'response_creation_time'
    template_name = 'search.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = (super().get_queryset().filter
            (
            response_post__in=Post.objects.filter
                (
                post_author=self.request.user).all()
                )
            )
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def response_accept(request, pk):
    response = Response.objects.get(id=pk)
    response.response_accepted = True
    response.save()
    response_accepter.apply_async([pk,],
                            eta=timezone.now() + datetime.timedelta(seconds=10))
    return redirect('/posts/search')


@login_required
def response_delete(request, pk):
    Response.objects.get(id=pk).delete()
    return redirect('/posts/search')