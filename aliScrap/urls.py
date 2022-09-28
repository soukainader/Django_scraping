from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('scraper.urls')),
]

urlpatterns += staticfiles_urlpatterns()
