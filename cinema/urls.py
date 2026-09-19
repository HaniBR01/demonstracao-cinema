from django.urls import path

from .views import cart_detail, home

urlpatterns = [
    path('', home, name='home'),
    path('carrinho/', cart_detail, name='cart-detail'),
]
