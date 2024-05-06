from django.contrib import admin

from .models import Article, ArticleCategory, Comment

class ArticleInLine(admin.StackedInline):
    model = Article

class CommentInLine(admin.StackedInline):
    model = Comment

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInLine,]


class ArticleAdmin(admin.ModelAdmin):
    model = Article


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)