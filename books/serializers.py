import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from books.models import Author, Book
from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from django_countries.serializers import CountryFieldMixin


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'publication_date',)


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='author-detail')
    # user = UserSerializer(required=True)
    user = HyperlinkedRelatedField(allow_null=True,
                                   queryset=get_user_model().objects.all(),
                                   required=False,
                                   validators=[UniqueValidator(queryset=Author.objects.all())],
                                   view_name='customuser-detail')
    books = BookSerializer(source="book_set", many=True, required=False)

    class Meta:
        model = Author
        fields = '__all__'

    def validate_short_name(self, short_name):
        if not re.match(r"[a-zA-Z]", short_name):
            raise serializers.ValidationError("Short Name must contain only alphabetical characters")
        else:
            return short_name

    def create(self, validated_data):
        books = validated_data.pop('book_set', None)
        author_created = Author.objects.create(**validated_data)
        if books is not None:
            for book in books:
                book = Book.objects.create(**book, author=author_created)
        return author_created
