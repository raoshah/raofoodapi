from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data