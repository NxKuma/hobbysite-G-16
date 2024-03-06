# Register your models here.
from django.contrib import admin
from .models import Article, ArticleCategory

class ArticleInLine(admin.StackedInline):
    model = ArticleCategory

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [ArticleInLine,]

admin.site.register(Article, ArticleAdmin)



