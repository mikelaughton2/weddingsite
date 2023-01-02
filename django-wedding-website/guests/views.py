import base64
from collections import namedtuple
import random
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from guests import csv_import
from guests.invitation import get_invitation_context, INVITATION_TEMPLATE, guess_party_by_invite_id_or_404, \
    send_invitation_email, get_RSVP_template_from_party
from guests.models import Guest, MEALS, Party
from guests.save_the_date import get_save_the_date_context, send_save_the_date_email, SAVE_THE_DATE_TEMPLATE, \
    send_all_save_the_dates
from .forms import ConfirmForm
from django.utils.translation import gettext as _
from babtynoemail.models import RSVPEmail
from babtyno.models import NewlyWedSetting, EmailSettings

class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
def dashboard(request):
    parties_with_pending_invites = Party.objects.filter(
        is_invited=True, is_attending=None
    ).order_by('category', 'name')
    parties_with_unopen_invites = parties_with_pending_invites.filter(invitation_opened=None)
    parties_with_open_unresponded_invites = parties_with_pending_invites.exclude(invitation_opened=None)
    attending_guests = Guest.objects.filter(is_attending=True)
    guests_without_meals = attending_guests.filter(
        is_child=False
    ).filter(
        Q(meal__isnull=True) | Q(meal='')
    ).order_by(
        'party__category', 'first_name'
    )
    meal_breakdown = attending_guests.exclude(meal=None).values('meal').annotate(count=Count('*'))
    category_breakdown = attending_guests.values('party__category').annotate(count=Count('*'))
    return render(request, 'guests/dashboard.html', context={
        'couple_name': NewlyWedSetting().newlyweds,
        'location': NewlyWedSetting().location,
        'guests': Guest.objects.filter(is_attending=True).count(),
        'possible_guests': Guest.objects.filter(party__is_invited=True).exclude(is_attending=False).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count(),
        'pending_invites': parties_with_pending_invites.count(),
        'pending_guests': Guest.objects.filter(party__is_invited=True, is_attending=None).count(),
        'guests_without_meals': guests_without_meals,
        'parties_with_unopen_invites': parties_with_unopen_invites,
        'parties_with_open_unresponded_invites': parties_with_open_unresponded_invites,
        'unopened_invite_count': parties_with_unopen_invites.count(),
        'total_invites': Party.objects.filter(is_invited=True).count(),
        'meal_breakdown': meal_breakdown,
        'category_breakdown': category_breakdown,
    })


def invitation(request, invite_id):
    party = guess_party_by_invite_id_or_404(invite_id)
    if party.invitation_opened is None:
        # update if this is the first time the invitation was opened
        party.invitation_opened = datetime.utcnow()
        party.save()
    if request.method == 'POST':
        for response in _parse_invite_params(request.POST):
            guest = Guest.objects.get(pk=response.guest_pk)
            assert guest.party == party
            guest.is_attending = response.is_attending
            #guest.meal = response.meal
            guest.save()
        if request.POST.get('comments'):
            comments = request.POST.get('comments')
            party.comments = comments if not party.comments else '{}; {}'.format(party.comments, comments)
        party.is_attending = party.any_guests_attending
        party.save()
        return HttpResponseRedirect(reverse('guests:rsvp-confirm', args=[invite_id]))
    return render(request, template_name='guests/invitation.html', context={
        'couple_name': NewlyWedSetting.for_site(1).newlyweds,
        'location': NewlyWedSetting.for_site(1).location,
        'party': party,
        'meals': MEALS,
        'main_image': 'bride-groom.png',
    })


InviteResponse = namedtuple('InviteResponse', ['guest_pk', 'is_attending', 'meal'])


def _parse_invite_params(params):
    responses = {}
    for param, value in params.items():
        if param.startswith('attending'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['attending'] = True if value == 'yes' else False
            responses[pk] = response
        elif param.startswith('meal'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['meal'] = value
            responses[pk] = response

    for pk, response in responses.items():
        yield InviteResponse(pk, response['attending'], response.get('meal', None))


def rsvp_confirm(request, invite_id=None):
    party = guess_party_by_invite_id_or_404(invite_id)
    template = get_RSVP_template_from_party(party)
    return render(request, template_name='guests/rsvp_confirmation.html', context={
        'party': party,
        'support_email': EmailSettings.for_site(1).default_wedding_email,
        'couple': NewlyWedSetting.for_site(1).newlyweds,
        'template':template,
    })


@login_required
def invitation_email_preview(request, invite_id):
    party = guess_party_by_invite_id_or_404(invite_id)
    #For now
    email = get_RSVP_template_from_party(party)
    context = get_invitation_context(party)
    context['email']=email
    context['invite_id'] = invite_id
    return render(request, INVITATION_TEMPLATE, context=context)


@login_required
def invitation_email_test(request, invite_id):
    party = guess_party_by_invite_id_or_404(invite_id)
    send_invitation_email(party, recipients=[settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse('sent!')

@login_required
def save_the_dates_send(request):
    to_send_to = Party.in_default_order().filter(is_invited=True, save_the_date_sent=None)
    if request.method == "POST":
        form = ConfirmForm(request.POST)
        if form.is_valid():
            test_only = form.cleaned_data['test_only']
            mark_sent = form.cleaned_data['mark_sent']
            send_all_save_the_dates(test_only = test_only,mark_as_sent=mark_sent)
            context = {}
            context['title']=("Successful test") if test_only else _("Sent!")
            context['message']="<p>"
            context['message']+=_("Sent!") if not test_only else _("Successful test")
            context['message']+="</p>"
            context['message']+="<p>"
            context['message']+=_("Marked sent") if mark_sent else _("Not marked sent")
            context['message']+="</p>"
        return render(request,"guests/admin_message.html",
            context=context)
    else:
        to_send_to = Party.in_default_order().filter(is_invited=True, save_the_date_sent=None)
        form = ConfirmForm()
        return render(request,"guests/proforma.html",
            context={'form':form,'title':_('Send save the dates?'),'to_send_to':to_send_to})

@login_required
def rsvp_send(request,party_pk):
    party_instance = get_object_or_404(Party,pk=int(party_pk))
    if request.method == "POST":
        form = ConfirmForm(request.POST)
        if form.is_valid():
            test_only = form.cleaned_data['test_only']
            mark_sent = form.cleaned_data['mark_sent']
            send_invitation_email(party_instance,test_only = test_only)
            context = {}
            context['title']=_("Successful test") if test_only else _("Sent!")
            context['message']="<p>"
            context['message']+=_("Sent!") if not test_only else _("Successful test")
            context['message']+="</p>"
            context['message']+="<p>"
            context['message']+=_("Marked sent") if mark_sent else _("Not marked sent")
            context['message']+="</p>"
        return render(request,"guests/admin_message.html",
            context=context)
    else:
        form = ConfirmForm()
        return render(request,"guests/proforma.html",
            context={'form':form,'title':_('Send RSVP to {}?'.format(party_instance.guest_emails)),'to_send_to':party_instance.guest_emails,'party':party_instance})

def save_the_date_preview(request, template_id):
    context = get_save_the_date_context(template_id)
    context['email_mode'] = False
    return render(request, SAVE_THE_DATE_TEMPLATE, context=context)


@login_required
def test_email(request, template_id):
    context = get_save_the_date_context(template_id)
    send_save_the_date_email(context, [settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse('sent!')


def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())
