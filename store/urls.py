from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cart/', views.CatView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView .as_view(), name='checkout'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('delete-orderitem/<pk>/', views.DeleteOrderItemView.as_view(), name='delete-order-item'),
]