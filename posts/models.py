from django.db import models

from users.models import CustomUser


class Post(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='posts')
    likes = models.ManyToManyField(CustomUser,
                                   related_name='likes',
                                   through='Like')

    def __str__(self):
        return f"Post by {self.author.full_name}"

    # TODO add updated on, required fields


class Like(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)




