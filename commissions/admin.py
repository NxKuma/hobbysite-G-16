from django.contrib import admin

from .models import Commission, Comment


class CommentInline(admin.StackedInline):
    model = Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    inlines = [CommentInline]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)