from django.contrib import admin

from .models import ThreadCategory, Thread, Comment


class ThreadInline(admin.StackedInline):
    model = Thread


class CommentInLine(admin.StackedInline):
    model = Comment


class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    inlines = [ThreadInline, ]


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    inlines = [CommentInLine, ]


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin) 