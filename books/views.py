from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from .models import Book, Author
from .forms import BookForm


def index(request):
    list_of_books = Book.objects.order_by('-id')
    template = loader.get_template('index.html')
    context = {'list_of_books': list_of_books}
    return HttpResponse(template.render(context, request))


def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        for field in form:
            print("Field Error:", field.name,  field.errors)
        if form.is_valid():
            author = Author.objects.get(pk=form.cleaned_data['author'].id)
            book = Book.objects.create(
                name=form.cleaned_data['name'],
                publication_year=form.cleaned_data['publication_year'],
                author=author
            )
            book.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BookForm()
        return render(request, 'create.html', {'form': form})


def read_or_update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(request.POST)
        for field in form:
            print("Field Error:", field.name,  field.errors)
        if form.is_valid():
            book.name = form.cleaned_data['name']
            book.publication_year = form.cleaned_data['publication_year']
            book.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BookForm(instance=book)
        return render(request, 'update.html', {'book': book, 'form': form})
