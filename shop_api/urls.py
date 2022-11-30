from django.urls import path

from .views import *

urlpatterns = [
    path('items/', ItemsAPIView.as_view(), name='all_items'),
    path('item/<int:pk>/', ItemDetailAPIView.as_view(), name='detail_item'),
    path('categories/', CategoriesAPIView.as_view(), name='all_categories')
]
