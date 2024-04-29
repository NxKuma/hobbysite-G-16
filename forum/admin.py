from django.contrib import admin

from .models import ThreadCategory, Thread


class ThreadInline(admin.StackedInline):
    model = Thread


class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    inlines = [ThreadInline, ]


class ThreadAdmin(admin.ModelAdmin):
    model = Thread


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin) 