from django.urls import path
from .views import MyOrderView, CreateOrderProductView, DeleteOrderProductView, CheckoutView, ReceiptView

urlpatterns = [
    path("mi-orden", MyOrderView.as_view(), name="my_order"),
    path("new_order", CreateOrderProductView.as_view(), name="new_order"),
    path("delete_product", DeleteOrderProductView.as_view(), name='delete_order_product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('receipt/<int:order_id>/', ReceiptView.as_view(), name='receipt'),
]
