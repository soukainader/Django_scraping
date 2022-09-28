from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home_view, name='home'),
    path('loading/', views.loading_view, name='loading'),
    path('datatable/', views.datatable_view, name='datatable')
   
]

urlpatterns += staticfiles_urlpatterns()
