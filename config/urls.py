from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('allauth.urls')),
    path('cart/', include('cart.urls')),
    path('api/v1/', include('shop_api.urls')),
    path('api/v1/cart/', include('cart_api.urls')),
    re_path(r'api/v1/auth/', include('djoser.urls.authtoken')),
    path('', include('shop.urls')),
] + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                        document_root=settings.MEDIA_ROOT)
