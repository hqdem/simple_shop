from rest_framework import serializers

from shop.models import ShopItem, Category


class ShopItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=ShopItem.objects.all(), slug_field='name')
    category_id = serializers.IntegerField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ShopItem
        fields = '__all__'

    def get_image(self, item):
        request = self.context.get('request')
        image = item.image
        if not image:
            return ''
        return request.build_absolute_uri(image.url)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['slug']
