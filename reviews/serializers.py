from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'category', 'created', 'updated']
        expandable_fields = {
            'category': (CategorySerializer, {'many': True})
        }
