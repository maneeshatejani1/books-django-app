from django.http.response import HttpResponse, HttpResponseRedirect

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from .models import Book, Author

def index(request):
    list_of_books = Book.objects.order_by('-id')
    template = loader.get_template('index.html')
    context = {'list_of_books': list_of_books}
    return HttpResponse(template.render(context,request))

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'detail.html', {'book': book})

def update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    print(book.id)
    bookname = request.POST['bookname'] 
    #TODO: need to implement serializer at this point since this is not getting saved in the database
    print(bookname)
    print(type(bookname))
    book.bookname = bookname
    book.save()
    print(book.name)
    return HttpResponseRedirect(reverse('index'))