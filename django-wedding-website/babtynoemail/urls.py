from django.urls import re_path, path
from .views import SaveTheDateEmailView, RSVPEmailView

app_name="babtynoemail"
urlpatterns = [
    path('std/<int:pk>/', SaveTheDateEmailView.as_view(),name='std-prev'),
    path('rsvpemail/<int:pk>',RSVPEmailView.as_view(),name='rsvp-prev'),
]
