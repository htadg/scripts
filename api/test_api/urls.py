from django.conf.urls import url, include
from django.contrib import admin
import products.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(products.urls), name="Product"),
]
