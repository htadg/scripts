from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<category>[\w\-]+)/$', getList, name="getList"),
    url(r'^product/(?P<category>[\w\-]+)/$', getProduct, name="getProduct"),
]
