from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from .models import Party, Guest, Menu, Dish
from guests.views import save_the_dates_send, rsvp_send, new_dashboard
from wagtail import hooks
from wagtail.admin.panels import FieldPanel
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse
from django.utils.translation import gettext as _
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.admin.panels import ObjectList
from django.db import models
from django import forms

class PartyExtraButtons(ButtonHelper):

    send_button_classnames = ["button-small","icon","icon-site"]
    #This needs fixing
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
    list_display = ("name","ordered_guests","guest_emails","any_guests_attending","save_the_date_sent","invitation_sent",)
    search_fields = ("name",)
    inspect_view_enabled = True
    # inspect_view_fields = ("guest_set",)
    button_helper_class = PartyExtraButtons
    panels = [
        FieldPanel("name",heading="Name"),
        FieldPanel("type",heading="Type"),
        FieldPanel("save_the_date_template",heading="Save the date template"),
        FieldPanel("save_the_date_sent",heading="Save the date sent"),
        FieldPanel("save_the_date_opened",heading="Save the date opened"),
        FieldPanel("rsvp_template",heading="RSVP Template"),
        FieldPanel("invitation_sent",heading="Invitation sent"),
        FieldPanel("invitation_opened",heading="Invitation opened"),
        FieldPanel("invitation_id"),
        FieldPanel("category",heading="Category"),
        FieldPanel("is_invited",heading="Is invited"),
        FieldPanel("rehearsal_dinner",heading="Rehearsal dinner"),
        FieldPanel("is_attending",heading="Is attending"),
        FieldPanel("comments",heading="Comments"),
        InlinePanel("guests",heading="Guests"),
    ]


class GuestAdmin(ModelAdmin):
    model = Guest
    menu_label = "Guests"
    menu_icon = "pick"
    menu_order = 151
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("first_name","last_name","party","email")
    search_fields=("first_name","last_name","party","email")
    list_filter=("party",)
    panels = [
        FieldPanel("party",heading="party"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("email"),
        FieldPanel("is_attending"),
        FieldPanel("is_child"),
        FieldPanel("meal"),
        FieldPanel("dishes",heading=_("Meal"),widget=forms.CheckboxSelectMultiple)
    ]

class PartyGuest(ModelAdminGroup):
    menu_label = "Guests"
    menu_icon = "group"
    menu_order = 150
    items = (PartyAdmin,GuestAdmin)

class MenuAdmin(ModelAdmin):
    model = Menu
    menu_label = "Food Menus"
    menu_icon = "group"
    menu_order = 200
    panels = [
        FieldPanel("name",heading="Name"),
        InlinePanel("dish",heading="Dishes",label="Dish"),
    ]

modeladmin_register(PartyAdmin)
modeladmin_register(GuestAdmin)
modeladmin_register(MenuAdmin)

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
            path('send_rsvps/',rsvps_send,name='send_rsvps'),
        ]

@hooks.register('register_admin_url')
def register_send_individual_RSVP():
    return [
        path('send-rsvp-individual/',rsvp_send,name='send-rsvp-individual'),
    ]

# @hooks.register('register_admin_menu_item')
# def register_rsvp_send_menu_item():
#     return MenuItem('Send RSVPs',reverse('guests:send-rsvps'),icon_name='envelope'),

@hooks.register('register_admin_urls')
def register_new_dashboard():
    return [
        path('new_dashboard/',new_dashboard,name='new_dashboard'),
    ]

@hooks.register('register_admin_menu_item')
def register_new_dashboard_item():
    return MenuItem('Dashboard',reverse('new_dashboard'),icon_name='order',order=0)
