from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('products/', views.product_list, name='product_list'),


    # path('booking/<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]