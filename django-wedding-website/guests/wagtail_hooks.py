from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from .models import Party, Guest
from guests.views import save_the_dates_send,rsvp_send
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse
from django.utils.translation import gettext as _

from django.db import models

class PartyExtraButtons(ButtonHelper):

    send_button_classnames = ["button-small","icon","icon-site"]

    def send_STD_button(self,obj):
        text = _("Send Save The Date")
        return {
            "url":reverse('guests:dashboard'), #send to home for now...
            "label": text,
            "classname": self.finalise_classname(self.send_button_classnames),
            "title": text
        }

    def send_RSVP_button(self,obj):
        text = _("Send RSVP")
        return {

            "url":reverse('guests:send-rsvp-individual',kwargs={'party_pk':obj.id}),
            "label":text,
            "classname": self.finalise_classname(self.send_button_classnames),
            "title":text,

        }

    def get_buttons_for_obj(self,obj,exclude=None,classnames_add=None,classnames_exclude=None):
        btns = super().get_buttons_for_obj(obj,exclude,classnames_add,classnames_exclude)
        for btn in ['send_STD','send_RSVP']:
            if btn not in (exclude or []):
                btns.append(getattr(self,"{}_button".format(btn))(obj))
        return btns

class PartyAdmin(ModelAdmin):
    model = Party
    menu_label = "Parties"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name","guest_emails","any_guests_attending")
    search_fields = ("name",)
    button_helper_class = PartyExtraButtons

class GuestAdmin(ModelAdmin):
    model = Guest
    menu_label = "Guests"
    menu_icon = "pick"
    menu_order = 201
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("first_name","last_name","party","email")
    search_fields=("first_name","last_name","party","email")
    list_filter=("party",)

class PartyGuest(ModelAdminGroup):
    menu_label = "Guests"
    menu_icon = "group"
    menu_order = 200
    items = (PartyAdmin,GuestAdmin)

modeladmin_register(PartyGuest)

@hooks.register('register_admin_url')
def register_send_stds():
    return [
        path('send_stds/',save_the_dates_send,name='send-save-the-dates')
    ]

@hooks.register('register_admin_menu_item')
def register_send_stds_menu_item():
    return MenuItem('Send STDs',reverse('guests:send-save-the-dates'),icon_name='date')

@hooks.register('register_admin_url')
def register_invitation():
        return [
            path('send_rsvps',rsvps_send,name='send_rsvps'),
        ]

@hooks.register('register_admin_url')
def register_send_individual_RSVP():
    return [
        path('send-rsvp-individual',rsvp_send,name='send-rsvp-individual')
    ]

@hooks.register('register_admin_menu_item')
def register_rsvp_send_menu_item():
    return MenuItem('Send RSVPs',reverse('guests:send-rsvps'),icon_name='envelope'),

