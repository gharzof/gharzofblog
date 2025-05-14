from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return f"/detail/{obj.slug}/"

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about']

    def location(self, item):
        return reverse(item)
