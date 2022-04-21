from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Product, Category, Company, ProductSize, ProductSite, Comment, Image
from django.contrib.auth.models import User


class CategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']
        expandable_fields = {
            'products': ('reviews.ProductSerializer', {'many': True})
        }


class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'content', 'created', 'updated']
        expandable_fields = {
            'category': ('reviews.CategorySerializer', {'many': True}),
            'sites': ('reviews.ProductSiteSerializer', {'many': True}),
            'comments': ('reviews.CommentSerializer', {'many': True}),
            'image': ('reviews.ImageSerializer', {'many': True}),
        }


class CompanySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'name', 'url']


class ProductSizeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['pk', 'name']


class ProductSiteSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductSite
        fields = ['pk', 'name', 'price', 'url', 'created', 'updated']
        expandable_fields = {
            'product': 'reviews.CategorySerializer',
            'product_size': 'reviews.ProductSizeSerializer',
            'company': 'reviews.CompanySerializer',
        }


class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'title', 'content', 'created', 'updated']
        expandable_fields = {
            'product': 'reviews.CategorySerializer',
            'user': 'reviews.UserSerializer',
        }


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user']


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='product_headshot'
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token
