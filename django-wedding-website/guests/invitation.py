from email.mime.image import MIMEImage
import os
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Party, MEALS
from babtynoemail.models import RSVPEmail
from django.utils.translation import gettext as _
from bigday import settings
from guests.emailhelpers import get_site_password
from django.shortcuts import get_object_or_404
from babtyno.models import NewlyWedSetting,EmailSettings

INVITATION_TEMPLATE = 'mail/guest_email.html'


def guess_party_by_invite_id_or_404(invite_id):
    #Return appropriate party by their invite ID.
    #This should succeed if there's a valid ID.
    #It should return a 404 if there is not.
    try:
        return Party.objects.get(invitation_id=invite_id)
    except Party.DoesNotExist:
        if settings.DEBUG:
            # in debug mode allow access by ID
            return Party.objects.get(id=int(invite_id))
        else:
            raise Http404()

def get_RSVP_template_from_party(party,preview_only=False):
    #This should return an RSVPEmail object associated with a party.
    try:
        return get_object_or_404(RSVPEmail,pk=party.rsvp_template.pk)
    except:
        if party is not None:
            raise Exception("No invite with pk; make sure party has an RSVP template.")

def get_invitation_context(party):
    template = get_RSVP_template_from_party(party)
    context = {
        'email':template,
        'invitation_id':party.invitation_id
    }
    context['title']=template.title
    context['header_filename']=template.header_image
    context['main_image']=template.hero_image
    #note en-gb v. en-ca from original
    context['main_color']=template.main_colour
    context['font_color']=template.font_colour
    context['rsvp_address'] = EmailSettings.for_site(1).default_wedding_reply_email
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = NewlyWedSetting.for_site(1).newlyweds
    #Do we actually need this??
    context['location'] = NewlyWedSetting.for_site(1).location
    context['date'] = NewlyWedSetting.for_site(1).wedding_date
    context['page_title'] = (NewlyWedSetting.for_site(1).newlyweds + _(' - Save the Date!'))
    context['site_pwd'] = get_site_password()
    context['meals'] = MEALS
    context['party'] = party
    return context

def send_invitation_email(party, test_only=False, recipients=None):
    if recipients is None:
        recipients = party.guest_emails
    if not recipients:
        print (_('===== WARNING: no valid email addresses found for {} ====='.format(party)))
        return

    context = get_invitation_context(party)
    context['email_mode'] = True
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = NewlyWedSetting.for_site(1).newlyweds
    template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    template_text = _("You're invited to {}'s wedding. To view this invitation, visit {} in any browser.".format(
        NewlyWedSetting.for_site(1).newlyweds,
        reverse('guests:invitation', args=[context['invitation_id']])
    ))
    subject = context['email']['subject']
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, EmailSettings.for_site(1).default_wedding_from_email, bcc=recipients,
                                 cc=settings.WEDDING_CC_LIST,
                                 reply_to=[EmailSettings.for_site(1).default_wedding_reply_email])
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
    print ('sending invitation to {} ({})'.format(party.name, ', '.join(recipients)))
    if not test_only:
        msg.send()


def send_all_invitations(test_only, mark_as_sent):
    to_send_to = Party.in_default_order().filter(is_invited=True, invitation_sent=None).exclude(is_attending=False)
    for party in to_send_to:
        send_invitation_email(party, test_only=test_only)
        if mark_as_sent:
            party.invitation_sent = datetime.now()
            party.save()
