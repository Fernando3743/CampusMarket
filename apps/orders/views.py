from django.shortcuts import redirect
from django.http import Http404

# Create your views here.

from django.views.generic import DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Order, OrderProduct
from .forms import OrderProductForm


class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()


class CreateOrderProductView(LoginRequiredMixin, CreateView):
    form_class = OrderProductForm
    success_url = reverse_lazy("my_order")

    def form_valid(self, form):
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )
        form.instance.order = order
        form.instance.quantity = 1
        form.save()
        return super().form_valid(form)

class DeleteOrderProductView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Obtener el ID del objeto OrderProduct a eliminar
        order_product_id = request.POST.get('order_product_id')
        print(order_product_id)
        
        if not order_product_id:
            return redirect('my_order')  # Si no se pasa un id, redirige de vuelta

        try:
            # Buscar el objeto OrderProduct por su ID y asegurarnos que pertenece al usuario
            order_product = OrderProduct.objects.get(
                id=order_product_id,
                order__user=request.user,  # Aseguramos que el producto pertenece al usuario
                order__is_active=True       # Solo eliminamos si la orden está activa
            )
            # Eliminar el objeto encontrado
            order_product.delete()
        except OrderProduct.DoesNotExist:
            # Si no se encuentra el producto, lanzamos un error 404 o simplemente no hacemos nada
            raise Http404("Producto no encontrado.")
            
        return redirect('my_order')  # Redirigir de vuelta a la vista de la orden