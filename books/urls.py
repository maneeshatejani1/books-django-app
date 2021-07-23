from django.urls import path

from books import views
from books.views import AuthorView, UserDetail

urlpatterns = [
    path('api/v1', views.api_root),
    path('', views.index, name='index'),
    path('new/', views.create, name='create'),
    path('<int:book_id>/read_or_update/', views.read_or_update, name='read_or_update'),
    path('authors/', AuthorView.as_view(), name='authors'),
    path('authors/<int:pk>', AuthorView.as_view(), name='author-detail'),
    path('users/<int:pk>', UserDetail.as_view(), name='customuser-detail')
]
