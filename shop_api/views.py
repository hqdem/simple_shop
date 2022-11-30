from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from shop.models import ShopItem, Category
from .serializers import ShopItemSerializer, CategorySerializer


class ItemsAPIView(ListAPIView):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'category__name']


class ItemDetailAPIView(RetrieveAPIView):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer


class CategoriesAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
