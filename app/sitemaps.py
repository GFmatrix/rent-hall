from django.contrib.sitemaps import Sitemap
from .models import Hall

class HallSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Hall.objects.all()

    def lastmod(self, obj):
        return obj.updated_at