from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    posted_by = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='posts')
    content = models.CharField(max_length=1000, blank=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked', blank=True)
    
    def serialize(self):
        return {
            "posted_by":self.posted_by.username,
            "content":self.content,
            "posted_at":self.posted_at.strftime("%b %d %Y, %I:%M %p"),
            "liked_by":[user.username for user in self.liked_by.all()]     
        }

    def __str__(self):
        return f'{self.posted_by.username} post.'
    
class Comment(models.Model):
    posted_by = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True, related_name='comments' )   
    posted_on = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=500, blank=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'f{self.posted_by} comment.'
    
    
class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True, unique=True, related_name='follows') 
    
    """     def exclude_this_user_from_options(self):
            FOLLOW_CHOICES = []
            all_users_excluding_this = User.objects.all().exclude(id = self.user)
            for allowed_choices in all_users_excluding_this:
                choices = (allowed_choices.username, allowed_choices.username)
                FOLLOW_CHOICES.append(choices)
            return FOLLOW_CHOICES
            
        FOLLOW_CHOICES = exclude_this_user_from_options() """
            
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')
     
    def __str__(self):
        return f'f{self.user} relationships.'
    
    
