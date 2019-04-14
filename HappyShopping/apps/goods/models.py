from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    """商品类别"""
    
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目")
    )
    
    
    name = models.CharField(default='', max_length=30, verbose_name='类别名', help_text='类别名')
    code = models.CharField(default='', max_length=30, verbose_name='类别名code', help_text='类别名code')
    desc = models.TextField(default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    # 自关联，方便类目级别扩展，不需要按照类目级别定义固定数目的模型类
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类目级别', related_name='sub_cat')
    # 是否显示在商品导航栏
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """品牌名"""
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name="商品类目")
    name = models.CharField(default='', max_length=30, verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(default='', max_length=300, verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=300, upload_to='brands/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """商品"""
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目")
    goods_sn = models.CharField(max_length=50, verbose_name="商品唯一货号")
    name = models.CharField(max_length=300, verbose_name="商品名")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简介")
    goods_desc = UEditorField(imagePath="goods/images/", width=1000, height=300, filePath='goods/files/',
                              default='', verbose_name="内容")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    sold_num = models.IntegerField(default=0, verbose_name="销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏量")
    goods_num = models.IntegerField(default=0, verbose_name="库存量")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    ship_free = models.BooleanField(verbose_name="是否承担运费")
    goods_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否是新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    add_time = models.DateTimeField(verbose_name="添加时间")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, related_name='category',verbose_name="商品类目")
    goods = models.ForeignKey(Goods, related_name='goods')

    class Meta:
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(models.Model):
    """商品详情页轮播图"""
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsBanner(models.Model):
    """商品轮播图"""
    goods = models.ForeignKey(Goods, verbose_name="商品")
    image = models.ImageField(upload_to='banner', verbose_name="轮播图")
    index = models.IntegerField(default=0, verbose_name="添加时间")
    add_time = models.DateTimeField(verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords

