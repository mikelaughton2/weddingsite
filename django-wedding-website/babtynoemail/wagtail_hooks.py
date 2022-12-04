from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse

from .models import SaveTheDateEmail,RSVPEmail

class SaveTheDateButtons(ButtonHelper):
    view_button_classnames = ["button-small","icon","icon-site"]

    def view_button(self,obj):
        text = "View"
        return {
            "url":obj.get_absolute_url(),
            "label": text,
            "classname": self.finalise_classname(self.view_button_classnames),
            "title":text,
        }

    def get_buttons_for_obj(self,obj,exclude=None,classnames_add=None,classnames_exclude=None):
        btns = super().get_buttons_for_obj(obj,exclude,classnames_add,classnames_exclude)
        if 'view' not in (exclude or []):
            btns.append(self.view_button(obj))
        return btns

@modeladmin_register
class SaveTheDateEmail(ModelAdmin):
    model = SaveTheDateEmail
    menu_label = 'Save The Dates'
    menu_icon = 'mail'
    menu_order = 300
    button_helper_class = SaveTheDateButtons

@modeladmin_register
class RSVPDateEmail(ModelAdmin):
    model = RSVPEmail
    menu_label = 'RSVP Emails'
    menu_icon = 'mail'
    menu_order = 400
    #button_helper_class = SaveTheDateButtons

hooks.register('register_admin_url')
def register_invitation():
        return [
            path('send_rsvps',rsvps_send,name='send_rsvps'),
        ]

@hooks.register('regsiter_admin_menu_item')
def register_rsvp_send_menu_item():
    return MenuItem('Send RSVPs',reverse('send-rsvps'),icon_name='envelope'),
