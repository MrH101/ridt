from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .models import User, Blog, Comment
from .forms import BlogForm, CommentForm
from django.contrib.auth.decorators import login_required




@login_required
def profile_view(request):
    return render(request, 'app/profile.html')

class DashboardView(LoginRequiredMixin, ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'app/dashboard.html'

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'app/create_blog.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Blog has been successfully created.")
        return super().form_valid(form)

class BlogReadView(LoginRequiredMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'app/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
        context['blog'] = blog
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))

        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment')
            return HttpResponse('Unauthorized', status=401)

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = self.request.user
            comment.blog = blog
            comment.save()
            messages.success(request, "Comment has been successfully posted.")
        else:
            messages.error(request, 'There was an error posting your comment')
        return redirect('app:blog_detail', pk=blog.pk)

class BlogAdminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'app/blog_admin.html'

    def test_func(self):
        return self.request.user.is_staff

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'app/update_blog.html'

    def form_valid(self, form):
        messages.success(self.request, "Blog has been successfully updated.")
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or self.request.user.is_staff

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'app/delete_blog.html'
    success_url = reverse_lazy('app:dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Blog has been successfully deleted.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or self.request.user.is_staff

class CommentAdminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'app/comment_admin.html'

    def test_func(self):
        return self.request.user.is_staff

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'app/update_comment.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment has been successfully updated.")
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or self.request.user.is_staff