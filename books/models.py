from django.db import models
from django.contrib.auth import get_user_model


class Author(models.Model):
    CLASSIC = 'Classic'
    FICTION = 'Fiction'
    COMEDY = 'Comedy'
    ROMANCE = 'Romance'
    HORROR = 'Horror'
    HISTORY = 'History'

    AREAS_OF_INTEREST = (
        (CLASSIC, 'Classic'),
        (FICTION, 'Fiction'),
        (COMEDY, 'Comedy'),
        (ROMANCE, 'Romance'),
        (HORROR, 'Horror'),
        (HISTORY, 'History'),
    )
    short_name = models.CharField(max_length=200)
    area_of_interest = models.CharField(max_length=300, null=True, choices=AREAS_OF_INTEREST, default=CLASSIC)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user', null=True)

    def __str__(self):
        return self.short_name


class Book(models.Model):
    name = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)
    performed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.message
