from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from books.models import Author, CustomLog


@receiver(post_delete, sender=Author)
def log_entry_for_delete_author(sender, instance, *args, **kwargs):
    message = "author instance with id {} deleted".format(instance.id)
    CustomLog.objects.create(message=message, performed_by=instance.user)


@receiver(post_save, sender=Author)
def log_entry_for_create_or_update_author(sender, instance, created, **kwargs):
    if created:
        message = "new author instance created with id {}".format(instance.id)
    else:
        message = "author with id {} updated".format(instance.id)
    CustomLog.objects.create(message=message, performed_by=instance.user)
