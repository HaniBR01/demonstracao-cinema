from django.shortcuts import render

from .models import Cart


def get_session_cart(request):
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
    if cart is None:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart


def home(request):
    cart = get_session_cart(request)
    return render(request, 'cinema/home.html', {'cart': cart})


def cart_detail(request):
    cart = get_session_cart(request)
    return render(request, 'cinema/cart_detail.html', {'cart': cart})