from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework import generics
from rest_framework.response import Response

from .serializers import GoodsSerializer, CategorySerializer
from .models import Goods, GoodsCategory


# class GoodsListView(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#    def get(self, request, format=None):
#        goods = Goods.objects.all()[:10]
#        goods_serializer = GoodsSerializer(goods, many=True)
#        return Response(goods_serializer.data)
#
#    def post(self, request):
#        # 将前端传送过来的数据保存到GoodsSerializer对象之中
#        serializer = GoodsSerializer(data=request.data)
#        # 如果前端传送了数据，则将其保存
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CAEATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

# class GoodsListView(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#    def get(self, request, format=None):
#        goods = Goods.objects.all()[:10]
#        goods_serializer = GoodsSerializer(goods, many=True)
#        return Response(goods_serializer.data)
#


# generics.py
# class ListAPIView(mixins.ListModelMixin, GenericAPIView)
# class CreateAPIView(mixins.CreateModelMixin, GenericAPIView)
# .....更多见源码


# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#    """
#    商品列表页
#    """
#    queryset = Goods.objects.all()[:10]
#    serializer_class = GoodsSerializer
#
#    def get(self, request, format=None):
#        return self.list(request, *args, **kwargs)


from rest_framework.pagination import PageNumberPagination


class GoodsPagination(PageNumberPagination):
    page_size = 10  # 每页显示10条数据
    # 前端通过page_size参数动态指定向后台获取多少条数据，后台根据数目计算页数，返回相应数据
    # 如：http://127.0.0.1:8000/goods/?p=2&page_size=20
    page_size_query_param = 'page_size'
    page_query_param = 'p'  # 查询参数显示信息
    max_page_size = 100  # 最多显示100页


# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表页
#     """
#
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     pagination_class = GoodsPagination


from django_filters.rest_framework import DjangoFilterBackend
from goods.filters import GoodsFilter
from rest_framework import filters


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，搜索，过滤，排序
    """
    # 获取数据对象
    queryset = Goods.objects.all()
    # 序列化
    serializer_class = GoodsSerializer
    # 分页
    pagination_class = GoodsPagination
    # 过滤·搜索              django 过滤       rest_framework 搜索     rest_framework 排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 过滤器
    filter_class = GoodsFilter
    # 搜索字段
    # ^：以该字段开头
    # =：精确查找
    # @：全局搜索
    # $：正则匹配
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 排序字段
    ordering_fields = ('sold_num', 'add_time')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer




