from django.test import TestCase
from guests.invitation import *
from guests.models import Party,Guest
from babtynoemail.models import RSVPEmail,SaveTheDateEmail
from wagtail.test.utils.form_data import nested_form_data, streamfield
import json

class InviteEmailTestCase(TestCase):
    def initialise(self):
        self.rsvp_initial = {
            'title':'RSVP Test',
            'language':('en-gb', 'English'),
            'subject':'Test email',
            'main_colour':'#ffffff',
            'font_colour':'#000000',
            # 'body': streamfield(
            #     [
            #         ('raw_html','Test test test'),
            #         ],
            #     ),
        }

        self.initial_email_context = {

        }

        self.std_initial = {
            'id': 1,
            'title': 'Save The Date (EN)',
            'language': "('en-gb', 'English')",
            'subject': 'Save the Date',
            'main_colour': '#fff3e8',
            'font_colour': '#666666',
            # 'body': streamfield(
            #     [
            #         ('text', 'Teest test test'),
            #     ]
            #     ),
            }

        self.guest_initial = {
            'id': 1,
            'party_id': 1,
            'first_name': 'Dad',
            'last_name': '/',
            'email': 'unknown@unknown.com',
            'is_attending': True,
            'meal': 'vegetarian',
            'is_child': False
            }

        self.page_initial = {

        }

    def setUp(self):
        self.initialise()
        self.rsvp_test = RSVPEmail.objects.create(
            **self.rsvp_initial
        )
        self.std_test = SaveTheDateEmail.objects.create(
            **self.std_initial
        )
        self.party = Party.objects.create(
            name="Testy",
            type="formal",
            save_the_date_template=self.std_test,
            rsvp_template=self.rsvp_test,
        )
        self.guest1 = Guest.objects.create(**self.guest_initial)

    def test_get_RSVP_template_from_party(self):
        self.assertEquals(get_RSVP_template_from_party(self.party),self.rsvp_test)

    def test_get_invitation_context(self):
        #Test whether the RSVP email gets passed to the context properly
        self.assertEquals(
            get_invitation_context(self.party).email,self.rsvp_test
        )
