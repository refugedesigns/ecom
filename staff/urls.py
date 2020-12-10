from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.StaffView.as_view(), name='staff'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('create-product/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete')

]