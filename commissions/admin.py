from django.contrib import admin

from .models import Commission, Comment


class CommentInline(admin.StackedInline):
    model = Comment


class CommentAdmin(admin.ModelAdmin):
    model = Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommentInline]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)