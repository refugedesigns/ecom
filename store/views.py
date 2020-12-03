from django.views.generic import ListView
from .models import Product


class ProductListView(ListView):
    template_name = 'store/product_list.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


