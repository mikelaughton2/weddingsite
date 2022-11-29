from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import Party, Guest
from guests.views import save_the_dates_send
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse

class PartyAdmin(ModelAdmin):
    model = Party
    menu_label = "Parties"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name","guest_emails","any_guests_attending")
    search_fields = ("name",)

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
    return MenuItem('Send STDs',reverse('send-save-the-dates'),icon_name='date')
