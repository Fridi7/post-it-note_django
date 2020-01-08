from django.contrib import admin

# Register your models here.

from .models import Post
# from posts.models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "created", "updated"]
    list_filter = ["created", "updated"]
    list_display_links = ["created", "updated"]
    search_fields = ["title", "content"]
    list_editable = ["title"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
