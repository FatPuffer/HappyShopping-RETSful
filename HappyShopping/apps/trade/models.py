from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods
# 获取重写的user模型
User = get_user_model()


class ShoppingCart(models.Model):
    """购物车"""
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    nums = models.IntegerField(default=0, verbose_name='购买数量')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """订单"""

    ORDER_STATUS = (
        ('success', '成功'),
        ('cancel', '取消'),
        ('wait', '待支付')
    )

    user = models.ForeignKey(User, verbose_name='用户')
    order_sn = models.CharField(max_length=30, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='交易号')
    pay_status = models.CharField(choices=ORDER_STATUS, max_length=10, verbose_name='支付状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    order_mount = models.FloatField(default=0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户信息
    address = models.CharField(max_length=100, default='', verbose_name='收货人地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='收货人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系电话')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


class OrderGoods(models.Model):
    """订单商品表"""
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods")
    goods = models.ForeignKey(Goods, verbose_name="商品")
    nums = models.IntegerField(default=0, verbose_name="商品数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
