from django.contrib import admin

from .models import PostCategory, Post


class PostInline(admin.StackedInline):
    model = Post


class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    inlines = [PostInline, ]


class PostAdmin(admin.ModelAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin) 