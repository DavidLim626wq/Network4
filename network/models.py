from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    postTitle =  models.CharField(max_length=64)
    postBody = models.TextField()
    postTime = models.DateTimeField(default=datetime.now, blank=True)
    postAuthor = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user")
    likes = models.IntegerField(default=0)

    def __str__(self):
        return '{} by {}'.format(self.postTitle, self.postAuthor)
    
    def serialize(self):
        return {"id": self.id, "likes": self.likes }

class Profile(models.Model):
    profilename = models.ForeignKey(User, on_delete = models.CASCADE, related_name="profilename")
    following = models.ForeignKey(User, on_delete = models.CASCADE, related_name="following")

    def __str__(self):
        return '{} follows {}'.format(self.profilename, self.following)

class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE,  related_name="likedpost")
    liker = models.ForeignKey(User, on_delete = models.CASCADE,  related_name="liker")

    def __str__(self):
        return '{} liked {} Post ID={}'.format(self.liker, self.post, self.post.id)