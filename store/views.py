import datetime
import json
from django.conf import settings
from django.contrib import messages
from django.views import generic
from django.http import JsonResponse
from .models import Product, OrderItem, Address, Payment
from django.shortcuts import get_object_or_404, reverse, redirect
from .utils import get_or_set_order_session
from .forms import AddToCartForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(generic.ListView):
    template_name = 'store/product_list.html'
    queryset = Product.objects.all()



class ProductDetailView(generic.FormView):
    template_name = 'store/product_detail.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('store:cart') # Reverse to Cart

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        item_filter = order.items.filter(
            product=product, 
            colors=form.cleaned_data['colors'],
            size=form.cleaned_data['size']
        )

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.product = product 
            new_item.order = order
            new_item.save()
        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context

class CatView(generic.TemplateView):
    template_name = 'store/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super(CatView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context

class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect('store:cart')


class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect('store:cart')

class DeleteOrderItemView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect('store:cart')

class CheckoutView(generic.FormView):
    template_name = 'store/checkout.html'
    form_class = AddressForm


    def get_success_url(self):
        return reverse('store:payment') 

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)

        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')
        selected_billing_address = form.cleaned_data.get('selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type='S',
                user=self.request.user,
                address_line_1=form.cleaned_data["shipping_address_line_1"],
                address_line_2=form.cleaned_data["shipping_address_line_2"],
                zip_code=form.cleaned_data["shipping_zip_code"],
                city=form.cleaned_data["shipping_city"],
            )
            order.shipping_address = address
           

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type='B',
                user=self.request.user,
                address_line_1=form.cleaned_data["billing_address_line_1"],
                address_line_2=form.cleaned_data["billing_address_line_2"],
                zip_code=form.cleaned_data["billing_zip_code"],
                city=form.cleaned_data["billing_city"],
            )
            order.billing_address = address
            order.save()

        messages.info(
            self.request, "You have successfully added your addresses"
        )
        return super(CheckoutView, self).form_valid(form)


    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context

class PaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'store/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['PAYPAL_CLIENT_ID'] = settings.PAYPAL_CLIENT_ID
        context['order'] = get_or_set_order_session(self.request)
        context['CALLBACK_URL'] = self.request.build_absolute_uri(reverse("store:thank-you"))
        return context 

class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body)
        print(body)
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            amount=float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='Paypal',
        )
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "Success"})

class ThankYouView(generic.TemplateView):
    template_name = 'store/thanks.html' 