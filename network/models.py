from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=1000, blank=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked', blank=True)
    
    def is_content_empty(self):
        return self.content == ''
    
    def serialize(self):
        return {
            "id":self.id,
            "posted_by":self.posted_by.username,
            "content":self.content,
            "posted_at":self.posted_at.strftime("%b %d %Y, %I:%M %p"),
            "liked_by":[user.username for user in self.liked_by.all()]     
        }

    def __str__(self):
        return f'{self.posted_by.username} post.'
      
class Connections(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True, unique=True, related_name='connections')          
    followers = models.ManyToManyField(User, related_name='followers', blank=True, null=True)
    following = models.ManyToManyField(User, related_name='following', blank=True, null=True)
     
    def __str__(self):
        return f'{self.user} connections.'
    
    
