from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Goods


 #class GoodsListView(APIView):
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

class GoodsListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)


