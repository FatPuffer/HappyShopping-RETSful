from django.views.generic.base import View

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]

        # Todo: 方式一，手动添加每一个需要返回的字段，进行序列化，日期和图片不能够被序列化
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        #
        # from django.http import HttpResponse
        # import json
        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        # Todo: 方式二，使用 model_to_dict 方法，直接序列化查询对象，日期和图片不能够被序列化
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        #
        # from django.http import HttpResponse
        # import json
        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        # Todo: 方式三，使用 serializer 方法直接序列化整个对象集
        # from django.core import serializers
        # from django.http import HttpResponse
        # json_data = serializers.serialize('json', goods)
        # return HttpResponse(json_data, content_type='application/json')

        # Todo: 方式三，使用 JsonResponse 直接返回json格式数据
        from django.core import serializers
        from django.http import JsonResponse
        import json
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)
