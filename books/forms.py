from django import forms
from .models import Book
# class BookForm(forms.Form):
#     name = forms.CharField(label='Name of Book', max_length=100)
#     publication_year = forms.DateField(label='Year of publication')
#     # name = forms.CharField(label='Author Name', max_length=100)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'publication_year', 'author']
        # exclude = ['id',]
