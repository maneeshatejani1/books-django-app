from django.urls import path

from books import views
from books.views import AuthorView, AuthorDetail

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.create, name='create'),
    path('<int:book_id>/read_or_update/', views.read_or_update, name='read_or_update'),
    path('authors/<int:pk>', AuthorDetail.as_view()),
    path('authors/', AuthorView.as_view()),
]
