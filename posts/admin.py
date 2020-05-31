from django.contrib import admin

from .models import Post, Like

admin.site.register(Post)
# admin.site.register(Like)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'liked_on')

