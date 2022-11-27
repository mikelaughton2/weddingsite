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

    def __str(self):
        return "{}, ({})".format(self.title,self.language)
