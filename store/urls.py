from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cart/', views.CatView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView .as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank-you'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('orders/<pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('delete-orderitem/<pk>/', views.DeleteOrderItemView.as_view(), name='delete-order-item'),
]