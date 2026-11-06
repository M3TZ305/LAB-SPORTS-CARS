from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('language/', include('django.conf.urls.i18n')),
    path("admin/", admin.site.urls),
    path("", include("showroom.urls")),
]
