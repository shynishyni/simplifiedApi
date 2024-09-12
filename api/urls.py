from django.urls import path
from django.http import HttpResponseNotFound
from . import views

def favicon_view(request):
    return HttpResponseNotFound()  # Or serve a static favicon file if available

urlpatterns = [
    path('favicon.ico/', favicon_view),
    path('user', views.userApi, name='userApi'),  # For creating a new item or getting all items
    path('user/<int:id>/', views.userApi, name='userApi'),  # For updating, retrieving, or deleting an item by ID
    path('login',views.login_api,name='login'),
    path('signup',views.signup_api,name='signup'),
    path('adddata',views.products,name='adddata'),
    path('getdata',views.getproducts,name='getdata'),
    path('getdata/<str:name>',views.getproducts,name='get_product_by_name'),
    path('updateWithLoc',views.create_user_profile,name='update_with_loc'),
    path('updateWithLoc/<str:username>', views.update_user_profile, name='update_user_profile'),
    path('update_favorites',views.update_favorites,name='update_favorites'),
    path('update_cart',views.update_cart,name="update_cart"),
    path('update_orders',views.update_orders,name='update_orders'),
    path('get_favorites/<str:username>',views.get_favorites,name='get_favorites'),
    path('get_cart/<str:username>',views.get_cart,name='get_cart'),
    path('get_orders/<str:username>',views.get_orders,name='get_orders'),
    path('update_mul_orders',views.update_mul_orders,name='update_mul_orders')
]
