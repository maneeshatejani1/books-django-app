from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from books.models import Book, Author
from books.forms import BookForm
from books.serializers import AuthorSerializer, UserSerializer
from books.permissions import IsSelf


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('authors', request=request, format=format),
    })


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user = get_object_or_404(get_user_model(), pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthenticated, IsSelf]

    def get(self, request, pk=None, format=None):
        if pk is None:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            author = get_object_or_404(Author, pk=pk)
            serializer = AuthorSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except IntegrityError:
                return Response({
                    "message": "Integrity Error"
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "message": "successfully created author",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        self.check_object_permissions(request, author)
        data = request.data
        serializer = AuthorSerializer(instance=author, data=data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        author = get_object_or_404(Author, pk=pk)
        self.check_object_permissions(request, author)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
