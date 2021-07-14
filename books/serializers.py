from rest_framework import serializers
from django.contrib.auth import get_user_model

from books.models import Author


class AuthorSerializer(serializers.Serializer):
    short_name = serializers.CharField(max_length=200)
    area_of_interest = serializers.CharField(max_length=200)
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        user_id = validated_data['user_id']
        short_name = validated_data['short_name']
        area_of_interest = validated_data['area_of_interest']

        user = get_user_model().objects.get(id=user_id)
        return Author.objects.create(short_name=short_name, area_of_interest=area_of_interest, user=user)

    def update(self, instance, validated_data):
        instance.short_name = validated_data.get('short_name', instance.short_name)
        instance.area_of_interest = validated_data.get('area_of_interest', instance.area_of_interest)
        instance.save()
        return instance
