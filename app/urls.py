from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from app.views import (
    profile_view,
)

app_name = 'app'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('create_blog/', views.BlogCreateView.as_view(), name='create_blog'),
    path('blog/<int:pk>/', views.BlogReadView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/update/', views.BlogUpdateView.as_view(), name='update_blog'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete_blog'),
    path('blog/admin/', views.BlogAdminView.as_view(), name='blog_admin'),
    path('comment/admin/', views.CommentAdminView.as_view(), name='comment_admin'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='update_comment'),
    path('profile/', profile_view, name='profile'),
]