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
       path('login_user',views.login_user,name="login_user"),
       path('logout',views.logout_view,name="logout"),
       path('signup',views.sign_up,name="signup"),
        path('track_orders',views.track_orders,name="track_orders"),
         path('order_details/<int:order_id>/',views.displayOrderDetail,name="order_details"),
       #   path('order_details/',views.displayOrderDetaildev,name="order_detail"),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)