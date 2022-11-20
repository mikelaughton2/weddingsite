from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import Party, Guest

class PartyAdmin(ModelAdmin):
    model = Party
    menu_label = "Parties"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)

class GuestAdmin(ModelAdmin):
    model = Guest
    menu_label = "Guests"
    menu_icon = "pick"
    menu_order = 201
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name","party",)

class PartyGuest(ModelAdminGroup):
    menu_label = "Guests"
    menu_icon = "group"
    menu_order = 200
    items = (PartyAdmin,GuestAdmin)

modeladmin_register(PartyGuest)
