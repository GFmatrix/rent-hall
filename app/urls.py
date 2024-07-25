from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import HallSitemap

sitemaps = {
    'halls': HallSitemap,
}

urlpatterns = [
    path('', views.HallList.as_view(), name='index'),
    path('hall/', views.HallList.as_view(), name='hall-index'),
    path('hall/<int:pk>/', views.HallDetail.as_view(), name='detail'),
    path('contract-template/', views.HallDetail.as_view(), name='detail'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('application/', views.ApplicationSearch.as_view(), name='application-status'),
    path('application/<str:application_id>/', views.ApplicationDetail.as_view(), name='application-detail'),
    path('application-file/<str:application_id>/', views.ApplicationFile.as_view(), name='application_file'),

    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",)
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)