from django import forms
from store.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "image",
            "description",
            "price",
            "available_colors",
            "available_sizes",
        ]