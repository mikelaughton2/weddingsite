from django.db import models

# Create your models here.

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel,InlinePanel
from wagtail import blocks
from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.settings.models import BaseGenericSetting, BaseSiteSetting, register_setting
from django.utils.translation import gettext as _
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

@register_setting
class NewlyWedSetting(BaseSiteSetting):
    newlyweds = models.CharField(max_length=150,default='Happy & Couple')
    wedding_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("Newlywed Setting")

@register_setting
class EmailSettings(BaseSiteSetting):
    default_wedding_email = models.EmailField(max_length=254,default='example@example.com')
    default_wedding_from_email = models.EmailField(max_length=254,default='example@example.com')
    default_wedding_reply_email = models.EmailField(max_length=254,default='example@example.com')
    
    class Meta:
        verbose_name = _("Email settings")

class HomePage(Page):
    hero_text = models.CharField(blank=True,max_length=200)
    hero_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    welcome_text = RichTextField(blank=True)
    itinerary_text = RichTextField(blank=True)
    about_venue = RichTextField(blank=True)
    tripanel_nav = StreamField([
        ('imageLink',blocks.StructBlock(
            [
                ('link', blocks.CharBlock(form_classname="link 1 url")),
                ('Text', blocks.CharBlock(form_classname="link 1 text")),
                ('image',ImageChooserBlock()),
            ]
        ))
    ], use_json_field=True, blank=True, max_num=3, min_num=3)
    content_panels = Page.content_panels + [
        FieldPanel('hero_text',help_text="Text to be shown in front of the couple's picture"),
        FieldPanel('welcome_text',help_text="Welcoming blurb"),
        FieldPanel('itinerary_text',help_text="Details of intinerary"),
        FieldPanel('about_venue',help_text="Blurb about our venue"),
        FieldPanel('hero_image',help_text="Gallery images"),
        FieldPanel('tripanel_nav',help_text="Pick the row of three pictures!"),
            ]
    template = "home.html"

class BlogPost(Page):
    pass

class SimplePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body',help_text="Your text")
    ]
    template = "simplepage.html"

class RSVP(Page):
    welcome_text = RichTextField(blank=True)
    template = "RSVP.html"
