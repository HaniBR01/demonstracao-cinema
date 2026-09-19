from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Cart(models.Model):
    """A shopping cart that can contain any kind of sellable item."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def total_price(self):
        return sum(
            (item.subtotal for item in self.items.all()),
            Decimal('0.00'),
        )

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def add_item(self, item_id, item_type, unit_price, quantity=1):
        """Add an item or increase the quantity of an existing item."""
        candidate = CartItem(
            cart=self,
            item_id=str(item_id),
            item_type=item_type,
            unit_price=unit_price,
            quantity=quantity,
        )
        candidate.clean_fields()
        item, created = self.items.get_or_create(
            item_id=str(item_id),
            item_type=item_type,
            defaults={'unit_price': unit_price, 'quantity': quantity},
        )
        if not created:
            item.unit_price = unit_price
            item.quantity += quantity
            item.full_clean()
            item.save(update_fields=('unit_price', 'quantity'))
        return item

    def remove_item(self, item_id, item_type, quantity=1):
        """Decrease an item's quantity and remove it when it reaches zero."""
        if quantity < 1:
            raise ValidationError({'quantity': 'Quantity must be greater than zero.'})
        item = self.items.get(item_id=str(item_id), item_type=item_type)
        if quantity >= item.quantity:
            item.delete()
            return None
        item.quantity -= quantity
        item.full_clean()
        item.save(update_fields=('quantity',))
        return item

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    """A generic line item identified by type and external item ID."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_id = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('cart', 'item_type', 'item_id'),
                name='unique_cart_item_kind',
            ),
        ]

    @property
    def subtotal(self):
        return self.unit_price * self.quantity