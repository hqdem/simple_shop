from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import ShopItem, Category


class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        return ShopItem.objects.prefetch_related('category').all()


class ItemsByCategoryView(ListView):
    template_name = 'shop/by_category.html'
    context_object_name = 'items'
    paginate_by = 1

    def get_queryset(self):
        return ShopItem.objects.select_related('category').filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
        return data


class DetailShopItemView(DetailView):
    template_name = 'shop/detail_item.html'
    context_object_name = 'item'

    def dispatch(self, request, *args, **kwargs):
        self.kwargs['query_item'] = ShopItem.objects.select_related('category').get(slug=self.kwargs['item_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.kwargs['query_item']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        items_by_category = ShopItem.objects.select_related('category').filter(
            category=self.kwargs['query_item'].category).exclude(pk=self.get_object().pk)
        paginate_by = 1
        paginator = Paginator(items_by_category, paginate_by)
        if paginator.num_pages > 1:
            data['is_paginated'] = True
        else:
            data['is_paginated'] = False
        page = self.request.GET.get('page', 1)
        data['items'] = paginator.get_page(page)
        data['page_obj'] = paginator.page(page)
        return data


class SearchView(ListView):
    template_name = 'shop/search_results.html'
    context_object_name = 'items'
    paginate_by = 1

    def get_queryset(self):
        q = self.request.GET.get('q')
        return ShopItem.objects.select_related('category').filter(Q(name__icontains=q) | Q(category__name__icontains=q))
