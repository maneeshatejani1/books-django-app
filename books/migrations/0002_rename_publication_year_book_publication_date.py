# Generated by Django 3.2.5 on 2021-07-06 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publication_year',
            new_name='publication_date',
        ),
    ]