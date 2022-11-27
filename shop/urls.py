from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search_results'),
    path('category/<slug:category_slug>/', ItemsByCategoryView.as_view(), name='items_by_category'),
    path('item/<slug:item_slug>/', DetailShopItemView.as_view(), name='detail_item'),
]
