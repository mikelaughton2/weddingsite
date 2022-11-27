from django.urls import re_path, path
from .views import SaveTheDateEmailView

urlpatterns = [
    path('std/<int:pk>/', SaveTheDateEmailView.as_view(),name='std-prev'),
]
