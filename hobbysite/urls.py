from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('commissions/', include('commissions.urls', namespace='commissions')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('blog/', include('blog.urls', namespace='blog')),
]
