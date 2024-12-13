from django.db import models

# Create your models here.

from django.db import models

from apps.users.models import User
from apps.products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_saved = models.BooleanField(default=False)  # Nuevo campo para carritos guardados
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total de la orden
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)  # Pedido finalizado

    def __str__(self):
        return f"order {self.id} by {self.user}"

    def complete_order(self):
        # Calcular el total de la orden sumando los productos
        self.total = sum(item.product.price * item.quantity for item in self.orderproduct_set.all())
        self.is_active = False  # Marcar la orden como completa
        self.save()
        return self.total


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.order} - {self.product}"
