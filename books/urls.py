from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.create, name='create'),
    path('<int:book_id>/read_or_update/', views.read_or_update, name='read_or_update'),
]
