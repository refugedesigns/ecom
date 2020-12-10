from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from store.models import Order



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'orders': Order.objects.filter(user=self.request.user, ordered=True)
        })
        return context

class HomeView(TemplateView):
    template_name = 'index.html'

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse('contact')

    def form_valid(self, form):
        messages.info(self.request, "Thanks for getting in touch. We have received your message")
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        full_message = f"""
            Received message below from {name}, {email} 

            ____________________________


            {message}
            """

        send_mail(
                subject = "Received contact form submission",
                message = full_message, 
                from_email = email, 
                recipient_list = [settings.NOTIFY_EMAIL]
            )
        return super(ContactView, self).form_valid(form)
