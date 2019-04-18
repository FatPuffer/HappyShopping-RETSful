"""HappyShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
from HappyShopping.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls  # 文档
from rest_framework.routers import DefaultRouter

# from goods.views_base import GoodsListView
# from goods.views import GoodsListView
from goods.views import GoodsListViewSet

router = DefaultRouter()

# 配置url
router.register(r'goods', GoodsListViewSet)


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # 登录

    # 路由注册
    url(r'^', include(router.urls)),

    # 文档接口
    url(r'docs/', include_docs_urls(title='乐购平台')),
]
