from django.contrib import admin
from django.urls import path

from .views import add_snack_to_cart, cart_detail, home, movie_detail, snack_catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('filmes/<slug:slug>/', movie_detail, name='movie-detail'),
    path('lanches/', snack_catalog, name='snack-catalog'),
    path('lanches/<slug:slug>/adicionar/', add_snack_to_cart, name='add-snack-to-cart'),
    path('carrinho/', cart_detail, name='cart-detail'),
]
