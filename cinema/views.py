from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Cart, Movie, Screening, Snack


def get_session_cart(request):
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
    if cart is None:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart


def home(request):
    cart = get_session_cart(request)
    upcoming_screenings = Screening.objects.filter(
        starts_at__gte=timezone.now(),
    ).order_by('starts_at')
    movies = Movie.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            'screenings',
            queryset=upcoming_screenings,
            to_attr='upcoming_screenings',
        ),
    )
    return render(request, 'cinema/home.html', {'cart': cart, 'movies': movies})


def movie_detail(request, slug):
    cart = get_session_cart(request)
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    screenings = movie.screenings.filter(starts_at__gte=timezone.now())
    return render(
        request,
        'cinema/movie_detail.html',
        {'cart': cart, 'movie': movie, 'screenings': screenings},
    )


def snack_catalog(request):
    cart = get_session_cart(request)
    snacks = Snack.objects.filter(is_active=True)
    return render(request, 'cinema/snack_catalog.html', {'cart': cart, 'snacks': snacks})


def add_snack_to_cart(request, slug):
    if request.method != 'POST':
        return redirect('snack-catalog')
    cart = get_session_cart(request)
    snack = get_object_or_404(Snack, slug=slug, is_active=True)
    cart.add_item(snack.slug, 'snack', snack.price)
    return redirect('snack-catalog')


def cart_detail(request):
    cart = get_session_cart(request)
    return render(request, 'cinema/cart_detail.html', {'cart': cart})
