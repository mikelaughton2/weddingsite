from django.shortcuts import render
from django.views.generic import DetailView
from .models import SaveTheDateEmail
# Create your views here.

class SaveTheDateEmailView(DetailView):
    queryset = SaveTheDateEmail.objects.all()
    template_name = "mail/guest_email.html"
    context_object_name="email"
