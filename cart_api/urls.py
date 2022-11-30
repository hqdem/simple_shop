from django.urls import path

from .views import (
    CartDetailAPIView,
    CartAddItemAPIView,
    CartRemoveAPIView,
    CartIncQuantityAPIView,
    CartDecQuantityAPIView,
    CartPurchaseAPIView,
    PaymentRedirectAPIView
)

urlpatterns = [
    path('cart_detail/', CartDetailAPIView.as_view(), name='api_cart_detail'),
    path('cart_add/<int:item_id>/', CartAddItemAPIView.as_view(), name='api_cart_add'),
    path('cart_remove/<int:item_id>/', CartRemoveAPIView.as_view(), name='api_cart_remove'),
    path('inc/<int:item_id>/', CartIncQuantityAPIView.as_view(), name='api_cart_inc'),
    path('dec/<int:item_id>/', CartDecQuantityAPIView.as_view(), name='api_cart_dec'),
    path('purchase/', CartPurchaseAPIView.as_view(), name='api_cart_purchase'),
    path('payment_redirect/', PaymentRedirectAPIView.as_view(), name='api_cart_payment_redirect'),
]
