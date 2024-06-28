from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('',views.index,name="home"),
       path('calculatePrice',views.calculatePrice,name="calculatePrice"),
       path('cartPage',views.cartPage,name="cartPage"),
       path('showCartItems',views.showCartItems,name="showCartItems"),
       path('create_order',views.create_order,name="create_order"),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)