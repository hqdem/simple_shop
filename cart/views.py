from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.cache import cache

from yookassa import Configuration, Payment
import uuid

from .cart import Cart
from shop.models import ShopItem


Configuration.account_id = 962210
Configuration.secret_key = 'test_be528ZeXOpKdYjviCWQxYTD6WhdY0J665UWc9CCuSuc'


@login_required
def cart_detail(request):
    cart = Cart(request)
    context = {
        'total_price': cart.get_total_price(),
    }
    return render(request, 'cart/cart_detail.html', context=context)


@login_required
@require_POST
def cart_add(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(ShopItem, slug=product_slug)
    cart.add(product)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def cart_remove(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(ShopItem, slug=product_slug)
    cart.remove(product.slug)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def cart_inc(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(ShopItem, slug=product_slug)
    cart.inc_quantity(product.slug)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def cart_dec(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(ShopItem, slug=product_slug)
    cart.dec_quantity(product.slug)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def purchase(request):
    cart = Cart(request)
    total_price = cart.get_total_price()
    payment = Payment.create({
        "amount": {
            "value": str(total_price),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/cart/payment_redirect/"
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())

    cache.set(f'{request.session.session_key}_payment_id', payment.id)
    return redirect(payment.confirmation.confirmation_url)


@login_required
def payment_redirect(request):
    payment_id = cache.get(f'{request.session.session_key}_payment_id', None)
    cache.delete(f'{request.session.session_key}_payment_id')
    if not payment_id:
        return redirect('home')

    payment = Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        cart = Cart(request)
        for item in cart:
            product = item['product']
            product.total_sold += item['quantity']
            product.save()
        cart.clear()
        return redirect('payment_success')
    elif payment.status == 'canceled':
        return redirect('payment_fail')
    return redirect('home')


@login_required
def after_success(request):
    return render(request, 'cart/success.html')


@login_required
def after_fail(request):
    return render(request, 'cart/fail.html')
