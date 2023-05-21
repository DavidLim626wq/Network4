from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "postTitle", "postAuthor")

class ProfileAdmin(admin.ModelAdmin):
    pass

class LikedPostAdmin(admin.ModelAdmin):
    list_display = ('post','liker')


admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(LikedPost, LikedPostAdmin)