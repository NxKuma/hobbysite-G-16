from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('django.contrib.auth.urls')),
    path('merchstore/', include('merchstore.urls', namespace='merchstore')),
    path('commissions/', include('commissions.urls', namespace='commissions')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('blog/', include('blog.urls', namespace='blog')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)