from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


class User(AbstractUser):
    pass


class ShopItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    caption = models.TextField(verbose_name='Описание', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Скидка')
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    image = models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/')
    total_sold = models.IntegerField(default=0, verbose_name='Количество продаж')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-total_sold']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('detail_item', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('items_by_category', args=[self.slug])
