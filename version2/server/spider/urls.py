from django.urls import path

from . import views

app_name = 'spider'
urlpatterns = [
    path('', views.index, name='index'),
    path('<title>/', views.detail, name='detail'),
]
