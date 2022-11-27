from decimal import Decimal
from django.conf import settings

from shop.models import ShopItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = request.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()
        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product):
        product_slug = product.slug
        if product_slug not in self.cart:
            price = product.sale_price
            if not price:
                price = product.price

            self.cart[product_slug] = {
                # 'product': product,
                'quantity': 1,
                'price': str(price)
            }
            self.update_total_price(product_slug)
            self.save()

    def update_total_price(self, product_slug):
        if product_slug in self.cart:
            item = self.cart[product_slug]
            item['total_price'] = str(Decimal(item['price']) * item['quantity'])
            self.save()

    def remove(self, product_slug):
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    def inc_quantity(self, product_slug):
        if product_slug in self.cart:
            self.cart[product_slug]['quantity'] += 1
            self.update_total_price(product_slug)

    def dec_quantity(self, product_slug):
        if product_slug in self.cart:
            if self.cart[product_slug]['quantity'] > 0:
                self.cart[product_slug]['quantity'] -= 1
                if not self.cart[product_slug]['quantity']:
                    del self.cart[product_slug]
                self.update_total_price(product_slug)
                self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.cart = dict()
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_slugs = self.cart.keys()
        products = ShopItem.objects.prefetch_related('category').filter(slug__in=product_slugs)

        for product in products:
            self.cart[product.slug]['product'] = product

        for key, item in self.cart.items():
            item['product'] = self.cart[key]['product']
            yield item

