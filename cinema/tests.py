from decimal import Decimal
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Cart, Movie, Screening


class CartTests(TestCase):
    def test_home_page_has_cart_tab(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carrinho')
        self.assertContains(response, '/carrinho/')

    def test_cart_page_is_available_for_session_cart(self):
        response = self.client.get('/carrinho/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seu carrinho está vazio')

    def test_cart_accepts_different_generic_item_types(self):
        cart = Cart.objects.create()

        ticket = cart.add_item('42', 'movie_ticket', Decimal('25.00'), 2)
        snack = cart.add_item('42', 'snack', Decimal('12.50'))

        self.assertEqual(cart.items.count(), 2)
        self.assertEqual(ticket.subtotal, Decimal('50.00'))
        self.assertEqual(snack.subtotal, Decimal('12.50'))
        self.assertEqual(cart.total_quantity, 3)
        self.assertEqual(cart.total_price, Decimal('62.50'))

    def test_adding_same_type_and_id_updates_quantity_and_price(self):
        cart = Cart.objects.create()

        cart.add_item(7, 'movie_ticket', Decimal('20.00'), 2)
        item = cart.add_item(7, 'movie_ticket', Decimal('22.00'), 1)

        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.unit_price, Decimal('22.00'))

    def test_remove_item_decreases_quantity_and_deletes_when_empty(self):
        cart = Cart.objects.create()
        cart.add_item('A1', 'snack', Decimal('10.00'), 3)

        item = cart.remove_item('A1', 'snack')
        self.assertEqual(item.quantity, 2)
        self.assertIsNone(cart.remove_item('A1', 'snack', 2))
        self.assertFalse(cart.items.exists())

    def test_item_rejects_zero_quantity_and_negative_price(self):
        cart = Cart.objects.create()
        item = cart.items.model(
            cart=cart,
            item_id='A1',
            item_type='snack',
            unit_price=Decimal('-1.00'),
            quantity=0,
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

        with self.assertRaises(ValidationError):
            cart.add_item('A1', 'snack', Decimal('1.00'), 0)

        with self.assertRaises(ValidationError):
            cart.remove_item('A1', 'snack', 0)


class CatalogueTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='A Chegada',
            slug='a-chegada',
            synopsis='Uma linguista é convocada após a chegada de naves misteriosas.',
            duration_minutes=116,
            classification='12 anos',
        )
        self.future_screening = Screening.objects.create(
            movie=self.movie,
            starts_at=timezone.now() + timedelta(days=1),
            auditorium='2',
            format='2D',
            language='Legendado',
        )

    def test_home_lists_active_movies_and_their_next_screening(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A Chegada')
        self.assertContains(response, 'Próxima sessão')
        self.assertContains(response, '/filmes/a-chegada/')

    def test_movie_detail_lists_only_upcoming_screenings(self):
        Screening.objects.create(
            movie=self.movie,
            starts_at=timezone.now() - timedelta(days=1),
            auditorium='1',
        )

        response = self.client.get('/filmes/a-chegada/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Próximas sessões')
        self.assertContains(response, 'Sala 2')
        self.assertNotContains(response, 'Sala 1')

    def test_inactive_movie_is_not_in_catalogue_or_detail_page(self):
        self.movie.is_active = False
        self.movie.save(update_fields=('is_active',))

        self.assertNotContains(self.client.get('/'), 'A Chegada')
        self.assertEqual(self.client.get('/filmes/a-chegada/').status_code, 404)
