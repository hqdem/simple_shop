from django.urls import path

from .views import *

urlpatterns = [
    path('cart_detail/', cart_detail, name='cart_detail'),
    path('add/<slug:product_slug>/', cart_add, name='cart_add'),
    path('remove/<slug:product_slug>/', cart_remove, name='cart_remove'),
    path('dec_quantity/<slug:product_slug>/', cart_dec, name='cart_dec_quantity'),
    path('inc_quantity/<slug:product_slug>/', cart_inc, name='cart_inc_quantity'),
    path('order/', purchase, name='purchase_cart'),
    path('payment_redirect/', payment_redirect, name='payment_redirect'),
    path('payment_success/', after_success, name='payment_success'),
    path('payment_fail/', after_fail, name='payment_fail'),
]
