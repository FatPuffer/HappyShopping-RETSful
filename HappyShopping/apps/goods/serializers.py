from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage


# class GoodsSerializer(serializers.Serializer):
#    name = serializers.CharField(required=True, max_length=100)
#    click_num = serializers.IntegerField(default=0)
#    goods_front_image = serializers.ImageField()
#
#    # drf 默认会将所有字段值放在 validated_data 参数中
#    def create(self, validated_data):
#        """
#        创建对象
#        """
#        return Goods.objects.create(**validated)
#

class CategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化
    """

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """

    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    商品轮播图片序列化
    """
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    # Goods模型类的外键(商品分类)，实现序列化嵌套
    category = CategorySerializer()
    # Goods模型类的外键(商品轮播图片)，实现序列化嵌套
    # 该变量名于外键中 related_name 参数值要保持一致
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"

