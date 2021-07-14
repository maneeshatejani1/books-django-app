from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from books.models import Book, Author
from books.forms import BookForm
from books.serializers import AuthorSerializer
from django.db import IntegrityError


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
                publication_date=form.cleaned_data['publication_date'],
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
            book.publication_date = form.cleaned_data['publication_date']
            book.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BookForm(instance=book)
        return render(request, 'update.html', {'book': book, 'form': form})


class AuthorView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        author = request.data.get('author')
        serializer = AuthorSerializer(data=author)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response({"message": "Integrity Error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "message": "successfully created author",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):
    def get(self, request, pk, format=None):
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        data = request.data.get('author')
        serializer = AuthorSerializer(instance=author, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        get_object_or_404(Author, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
