from django.contrib import admin
from django.urls import path

from .views import cart_detail, home, movie_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('filmes/<slug:slug>/', movie_detail, name='movie-detail'),
    path('carrinho/', cart_detail, name='cart-detail'),
]
