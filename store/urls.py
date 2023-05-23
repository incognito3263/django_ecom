from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_user/', views.update_user_order, name='update_user'),
    path('process_order/', views.process_order, name='process_order')
]