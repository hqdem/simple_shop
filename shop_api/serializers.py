from rest_framework import serializers

from shop.models import ShopItem, Category


class ShopItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=ShopItem.objects.all(), slug_field='name')
    category_id = serializers.IntegerField()

    class Meta:
        model = ShopItem
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['slug']
