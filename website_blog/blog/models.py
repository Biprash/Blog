from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table='Post'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    comment_text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        db_table='Comment'

    def approve(self):
        self.approved_comment = timezone.now()
        self.save()

    def __str__(self):
    
        return self.comment_text