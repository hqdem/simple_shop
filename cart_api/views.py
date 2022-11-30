from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cart.cart import Cart
from shop.models import ShopItem
from shop_api.serializers import ShopItemSerializer
from .serializers import CartSerializer

from yookassa import Configuration, Payment
import uuid

Configuration.account_id = 962210
Configuration.secret_key = 'test_be528ZeXOpKdYjviCWQxYTD6WhdY0J665UWc9CCuSuc'


class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        res = CartSerializer(cart, many=True, context={'request': request}).data
        return Response(res)


class CartAddItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = Cart(request)
        product = get_object_or_404(ShopItem, id=item_id)
        cart.add(product)
        res = ShopItemSerializer(product).data
        return Response(res)


class CartRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = Cart(request)
        product = get_object_or_404(ShopItem, id=item_id)
        cart.remove(product.slug)
        res = ShopItemSerializer(product).data
        return Response(res)


class CartIncQuantityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = Cart(request)
        product = get_object_or_404(ShopItem, id=item_id)
        cart.inc_quantity(product.slug)
        res = ShopItemSerializer(product).data
        return Response(res)


class CartDecQuantityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = Cart(request)
        product = get_object_or_404(ShopItem, id=item_id)
        cart.dec_quantity(product.slug)
        res = ShopItemSerializer(product).data
        return Response(res)


class CartPurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        payment = Payment.create({
            "amount": {
                "value": str(total_price),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/api/v1/cart/payment_redirect/"
            },
            "capture": True,
            "description": "Заказ №1"
        }, uuid.uuid4())

        cache.set(f'{request.session.session_key}_payment_id', payment.id)
        return Response({
            'payment_url': payment.confirmation.confirmation_url,
        }, status=HTTP_200_OK)


class PaymentRedirectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payment_id = cache.get(f'{request.session.session_key}_payment_id', None)
        cache.delete(f'{request.session.session_key}_payment_id')
        if not payment_id:
            return Response({
                'detail': 'Оплата не прошла',
            }, status=HTTP_400_BAD_REQUEST)

        payment = Payment.find_one(payment_id)
        if payment.status == 'succeeded':
            cart = Cart(request)
            for item in cart:
                product = item['product']
                product.total_sold += item['quantity']
                product.save()
            cart.clear()
            return Response({
                'detail': 'Успешная оплата!',
            }, status=HTTP_200_OK)
        elif payment.status == 'canceled':
            return Response({
                'detail': 'Оплата не прошла. Попробуйте еще раз',
            }, status=HTTP_400_BAD_REQUEST)
        return Response({
            'detail': 'Ожидается оплата'
        }, status=HTTP_200_OK)
