from django.shortcuts import render
from django.views.generic import DetailView
from .models import SaveTheDateEmail, RSVPEmail
# Create your views here.

class SaveTheDateEmailView(DetailView):
    model = SaveTheDateEmail
    template_name = "mail/guest_email.html"
    context_object_name="email"

class RSVPEmailView(DetailView):
    model = RSVPEmail
    template_name = "mail/guest_email.html"
    context_object_name = "email"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)

        return context
