import django_filters
from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """商品过滤类"""
    # 过滤条件
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    # 模糊查询: i 表示不区分大小写
    # name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        # fields = ['price_min', 'price_max', 'name']
        fields = ['price_min', 'price_max']
