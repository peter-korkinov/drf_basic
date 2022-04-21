from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_flex_fields import is_expanded
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ProductSerializer, ImageSerializer, MyTokenObtainPairSerializer
from .models import Product, Image


class ProductViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permit_list_expand = ['category', 'sites', 'comments', 'site.company', 'sites.product_size']
    filterset_fields = ('category',)

    def get_queryset(self):
        queryset = Product.objects.all()

        if is_expanded(self.request, 'category'):
            queryset = queryset.prefetch_related('category')

        if is_expanded(self.request, 'comments'):
            queryset = queryset.prefetch_related('comments')

        if is_expanded(self.request, 'sites'):
            queryset = queryset.prefetch_related('sites')

        if is_expanded(self.request, 'company'):
            queryset = queryset.prefetch_related('sites__company')

        if is_expanded(self.request, 'product_size'):
            queryset = queryset.prefetch_related('sites__product_size')

        return queryset


class ImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
