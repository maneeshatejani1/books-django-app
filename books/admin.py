from django.contrib import admin

from books.models import Book, Author, CustomLog

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(CustomLog)
