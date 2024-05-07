from rest_framework import serializers
from ..entity_models.book import book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = book
        fields = "__all__"

