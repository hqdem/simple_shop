from rest_framework import serializers

from shop_api.serializers import ShopItemSerializer


class CartSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    product = ShopItemSerializer()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
