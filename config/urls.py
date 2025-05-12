from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog import sitemaps

sitemaps = {
    'posts': sitemaps.PostSitemap,
    'static': sitemaps.StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

handler404 = 'blog.views.custom_404'
