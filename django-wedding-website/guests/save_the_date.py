from __future__ import unicode_literals, print_function
from copy import copy
from email.mime.image import MIMEImage
import os
from datetime import datetime
import random
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from guests.models import Party
from babtynoemail.models import SaveTheDateEmail as STD
from guests.emailhelpers import get_site_password

SAVE_THE_DATE_TEMPLATE = 'mail/guest_email.html'


# SAVE_THE_DATE_CONTEXT_MAP = {
#
#     'title': 'whatever-the-database-says',
#     'hero-image': 'whatever-the-database-says',
#     'main colour': 'whatever the database says',
#     'text colour': 'whatever the database says',
# }

# Get template from Party needs to be reformed to select choose from a guest email in the database

#Delete this
SAVE_THE_DATE_CONTEXT_MAP = {
        'lions-head': {
            'title': "Lion's Head",
            'header_filename': 'hearts.png',
            'main_image': 'lions-head.jpg',
            'main_color': '#fff3e8',
            'font_color': '#666666',
        },
        'ski-trip': {
            'title': 'Ski Trip',
            'header_filename': 'hearts.png',
            'main_image': 'ski-trip.jpg',
            'main_color': '#330033',
            'font_color': '#ffffff',
        },
        'canada': {
            'title': 'Canada!',
            'header_filename': 'maple-leaf.png',
            'main_image': 'canada-cartoon-resized.jpg',
            'main_color': '#ea2e2e',
            'font_color': '#e5ddd9',
        },
        'american-gothic': {
            'title': 'American Gothic',
            'header_filename': 'hearts.png',
            'main_image': 'american-gothic.jpg',
            'main_color': '#b6ccb5',
            'font_color': '#000000',
        },
        'plunge': {
            'title': 'The Plunge',
            'header_filename': 'plunger.png',
            'main_image': 'plunge.jpg',
            'main_color': '#b4e6ff',
            'font_color': '#000000',
        },
        'dimagi': {
            'title': 'Dimagi',
            'header_filename': 'commcare.png',
            'main_image': 'join-us.jpg',
            'main_color': '#003d71',
            'font_color': '#d6d6d4',
        }
    }


def send_all_save_the_dates(test_only=False, mark_as_sent=False):
    to_send_to = Party.in_default_order().filter(is_invited=True, save_the_date_sent=None)
    for party in to_send_to:
        send_save_the_date_to_party(party, test_only=test_only)
        print(party)
        if mark_as_sent:
            party.save_the_date_sent = datetime.now()
            party.save()

def send_save_the_date_to_party(party, test_only=False):
    context = get_save_the_date_context(get_template_id_from_party(party))
    recipients = party.guest_emails
    if not recipients:
        print('===== WARNING: no valid email addresses found for {} ====='.format(party))
    else:
        print(recipients)
        send_save_the_date_email(
            context,
            recipients,
            test_only=test_only
        )

def get_template_id_from_party(party):
    #Dummy function for now - return the pk of the first obj
    try:
        return get_object_or_404(SaveTheDateEmail,pk=party.pk)
    except:
        return STD.objects.first().id

def get_save_the_date_context(template_id):
    template = get_object_or_404(STD,pk=template_id)
    context = {
        'email':template,
    }
    context['title']=template.title
    context['header_filename']=template.header_image
    context['main_image']=template.hero_image
    #note en-gb v. en-ca from original
    context['main_color']=template.main_colour
    context['font_color']=template.font_colour
    context['rsvp_address'] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    context['location'] = settings.WEDDING_LOCATION
    context['date'] = settings.WEDDING_DATE
    context['page_title'] = (settings.BRIDE_AND_GROOM + _(' - Save the Date!'))
    context['site_pwd'] = get_site_password()
    return context

def send_save_the_date_email(context, recipients, test_only=False):
    print(context)
    context['email_mode'] = True
    context['rsvp_address'] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(SAVE_THE_DATE_TEMPLATE, context=context)
    template_text = ("Save the date for " + settings.BRIDE_AND_GROOM + "'s wedding! " + settings.WEDDING_DATE + ". " + settings.WEDDING_LOCATION)
    subject = context['email'].subject
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, settings.DEFAULT_WEDDING_FROM_EMAIL, bcc=recipients, reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['header_filename'], context['main_image']):
        attachment_path = filename.file.path
        try:
            with open(attachment_path, "rb") as image_file:
                msg_img = MIMEImage(image_file.read())
                msg_img.add_header('Content-ID', '<{}>'.format(filename))
                msg.attach(msg_img)
                print("attached file fine")
        except:
            raise Exception("This attachment does not exist!")
            print("error attaching file")

    if not test_only:
        msg.send()


def clear_all_save_the_dates():
    print('clear')
    for party in Party.objects.exclude(save_the_date_sent=None):
        party.save_the_date_sent = None
        print("resetting {}".format(party))
        party.save()
