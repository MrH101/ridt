from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='created_blogs')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('app:blog_detail', args=[str(self.pk)])

class Comment(models.Model):
    content = models.TextField()
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='created_comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        ordering = ['-create_timestamp']
    
    def __str__(self):
        return f"Comment by {self.created_by} on {self.blog}"

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    interests = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
