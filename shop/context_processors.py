from .models import Category
from cart.cart import Cart


def add_all_categories(request):
    return {
        'categories': Category.objects.all(),
    }


def add_cart(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count_items': len(cart.cart.keys())
    }
