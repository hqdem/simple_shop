from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ShopItem, Category


class ShopItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    fields = ['name', 'caption', 'slug', 'price', 'sale_price', 'category', 'image', 'total_sold']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    fields = ['name', 'slug']


admin.site.register(User, UserAdmin)
admin.site.register(ShopItem, ShopItemAdmin)
admin.site.register(Category, CategoryAdmin)
