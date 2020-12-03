from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'store'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug>/', ProductDetailView.as_view(), name='product-detail'),
]