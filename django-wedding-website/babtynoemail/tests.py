from django.test import TestCase
from django.test import RequestFactory

from .views import *
# Create your tests here.

class EmailViewWorks(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.get(reverse('babtynoemail:rsvp-prev'))
        view = RSVPEmailView()
        view.setup(request)
        self.assertEquals(request.status_code,200)
