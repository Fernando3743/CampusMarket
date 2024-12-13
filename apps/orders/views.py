from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages

# Create your views here.

from django.views.generic import DetailView, CreateView, View, TemplateView
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
    
class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        # Buscar el pedido activo del usuario
        order = Order.objects.filter(user=request.user, is_active=True).first()

        if not order:
            messages.error(request, "No se encontró un pedido activo.")
            return redirect('my_order')  # Redirige a la vista de los pedidos

        # Completar la orden
        total = order.complete_order()

        # Aquí puedes agregar lógica para procesar el pago (como integración con un servicio de pago)

        # Mostrar el recibo
        messages.success(request, "¡Compra finalizada exitosamente! Puedes ver tu recibo a continuación.")
        return redirect('receipt', order_id=order.id)  # Redirige al recibo


class ReceiptView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = Order.objects.filter(id=order_id, user=request.user).first()

        if not order:
            messages.error(request, "No se encontró el recibo.")
            return redirect('my_order')

        order_products = order.orderproduct_set.all()

        context = {
            'order': order,
            'order_products': order_products,
        }
        return render(request, 'orders/receipt.html', context)
    
class SavedCartsView(LoginRequiredMixin, View):
    def get(self, request):
        # Obtener los carritos guardados del usuario actual
        saved_carts = Order.objects.filter(
            user=request.user, 
            is_saved=True, 
            is_active=False
        )
        print(saved_carts)  # Debugging: Verificar si hay carritos guardados

        context = {
            'saved_carts': saved_carts,
        }
        return render(request, 'orders/saved_carts.html', context)

    def post(self, request):
        print("Guardando carrito...")  # Esto te dirá si entra a la vista
        order = Order.objects.filter(user=request.user, is_active=True).first()
        if not order:
            messages.error(request, "No tienes un carrito activo para guardar.")
            return redirect('my_order')

        order.is_active = False
        order.is_saved = True
        order.save()
        messages.success(request, "Carrito guardado exitosamente.")
        print("Carrito guardado correctamente.")  # Confirmación de ejecución
        return redirect('my_order')



class RestoreCartView(View):
    def post(self, request, cart_id):
        # Obtener el carrito guardado
        saved_cart = Order.objects.filter(id=cart_id, user=request.user, is_saved=True).first()

        if not saved_cart:
            messages.error(request, "Carrito no encontrado o ya restaurado.")
            return redirect('saved_carts')

        # Desactivar otros carritos activos
        Order.objects.filter(user=request.user, is_active=True).update(is_active=False)

        # Restaurar el carrito guardado
        saved_cart.is_active = True
        saved_cart.is_saved = False
        saved_cart.save()

        messages.success(request, "Carrito restaurado correctamente.")
        return redirect('my_order')