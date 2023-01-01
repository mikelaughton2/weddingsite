from django.db import models
from wagtail.admin.edit_handlers import FieldPanel,FieldRowPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel,InlinePanel
from wagtail import blocks
from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, Orderable
from django import forms
from django.urls import reverse
from bigday import settings

class SaveTheDateEmail(models.Model):
    title = models.CharField(max_length=200,null=True)
    language = models.CharField(max_length=25,choices=settings.WAGTAIL_CONTENT_LANGUAGES,default=settings.WAGTAIL_CONTENT_LANGUAGES[0])
    header_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    subject = models.CharField(max_length=200,null=True)
    main_colour = models.CharField(max_length=9,default="#FFFFFF")
    font_colour = models.CharField(max_length=9,default="#000000")
    colour_widget = forms.TextInput(
        attrs = {
            'placeholder':'#FFFFFF',
            'type':'color',
        }
    )
    body = StreamField(
        [
        ('body',blocks.RichTextBlock(features=['h3','h4','bold','italic','link','ul','ol','document-link']))
        ],
        use_json_field=True
    )
    hero_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    panels = [
        FieldPanel('title',help_text="Name of email (internal only)"),
        FieldPanel('subject',help_text="Subject line - recipient sees this"),
        FieldPanel('header_image',help_text="Cute lil photo"),
        FieldRowPanel(
            [
                FieldPanel('main_colour',help_text="Main/background colour",widget=colour_widget),
                FieldPanel('font_colour',help_text="Text colour",widget=colour_widget)
            ]
                ),
        FieldPanel('body',help_text="Text of email"),
        FieldPanel('hero_image',help_text="Pretty image"),
    ]

    def get_absolute_url(self):
        return reverse('babtynoemail:std-prev',args=[str(self.id)])

    def __str__(self):
        return "{}".format(self.title)

class RSVPEmail(models.Model):
    title = models.CharField(max_length=200,null=True)
    language = models.CharField(max_length=25,choices=settings.WAGTAIL_CONTENT_LANGUAGES,default=settings.WAGTAIL_CONTENT_LANGUAGES[0])
    header_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    subject = models.CharField(max_length=200,null=True)
    main_colour = models.CharField(max_length=9,default="#FFFFFF")
    font_colour = models.CharField(max_length=9,default="#000000")
    colour_widget = forms.TextInput(
        attrs = {
            'placeholder':'#FFFFFF',
            'type':'color',
        }
    )
    body = StreamField(
        [
        ('body',blocks.RichTextBlock(features=['h3','h4','bold','italic','link','ul','ol','document-link']))
        ],
        use_json_field=True
    )
    hero_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    rsvp_positive_response_text = RichTextField(blank=True)
    rsvp_negative_response_text = RichTextField(blank=True)
    panels = [
        FieldPanel('title',help_text="Name of email (internal only)"),
        FieldPanel('subject',help_text="Subject line - recipient sees this"),
        FieldPanel('header_image',help_text="Cute lil photo at the top of the email"),
        FieldRowPanel(
            [
                FieldPanel('main_colour',help_text="Main/background colour",widget=colour_widget),
                FieldPanel('font_colour',help_text="Text colour",widget=colour_widget)
            ]
                ),
        FieldPanel('body',help_text="Text of email"),
        FieldPanel('hero_image',help_text="Pretty image in the email"),
        FieldPanel('rsvp_positive_response_text',help_text="Response to give the guests saying 'yes'"),
        FieldPanel('rsvp_negative_response_text',help_text="Response to give the guests saying 'no'. Make it nice!")
    ]

    def get_absolute_url(self):
        return reverse('guests:invitation-email',args=[str(self.id)])

    def __str__(self):
        return "{}".format(self.title)
