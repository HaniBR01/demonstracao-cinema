from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Cart, Movie, Screening


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
    screenings = movie.screenings.filter(starts_at__lte=timezone.now())
    return render(
        request,
        'cinema/movie_detail.html',
        {'cart': cart, 'movie': movie, 'screenings': screenings},
    )


def cart_detail(request):
    cart = get_session_cart(request)
    return render(request, 'cinema/cart_detail.html', {'cart': cart})
