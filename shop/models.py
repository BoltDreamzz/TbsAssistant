# shop/models.py

from django.db import models
from django.utils import timezone

class Product(models.Model):
    """Model representing a product in the shop."""
    # Assuming you have a Product model with fields like name, price, etc.
    # You can customize this model as per your requirements.
    name = models.CharField(max_length=255)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    flash_sale_start = models.DateTimeField(null=True, blank=True)
    flash_sale_end = models.DateTimeField(null=True, blank=True)
    descriptyion = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True, default='default.jpg')
    description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)  # Add stock field

    # Other fields like description, image, etc.

    def is_flash_sale_active(self):
        now = timezone.now()
        return self.flash_sale_start and self.flash_sale_end and self.flash_sale_start <= now <= self.flash_sale_end

    def get_current_price(self):
        if self.is_flash_sale_active() and self.discount_price:
            return self.discount_price
        return self.normal_price

    def flash_sale_remaining_seconds(self):
        """Return seconds remaining for countdown."""
        if self.is_flash_sale_active():
            return int((self.flash_sale_end - timezone.now()).total_seconds())
        return 0


# cart/models.py

from django.db import models
from django.contrib.auth.models import User
# from shop.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.get_current_price() * self.quantity
