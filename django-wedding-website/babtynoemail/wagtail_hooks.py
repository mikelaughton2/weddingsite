from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse

from .models import SaveTheDateEmail

@modeladmin_register
class SaveTheDateEmail(ModelAdmin):
    model = SaveTheDateEmail
    menu_label = 'Save The Date Emails'
    menu_icon = 'mail'
    menu_order = 300
