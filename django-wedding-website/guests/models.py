from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from wagtail.models import Orderable,ClusterableModel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.admin.panels import ObjectList
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as pg_
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail.admin.panels import FieldPanel
from wagtail.admin.edit_handlers import InlinePanel

# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('formal', 'formal'),
    ('fun', 'fun'),
    ('dimagi', 'dimagi'),
]


def _random_uuid():
    return uuid.uuid4().hex


class Party(ClusterableModel):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    type = models.CharField(max_length=10, choices=ALLOWED_TYPES)
    save_the_date_template = models.ForeignKey("babtynoemail.SaveTheDateEmail",
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    rsvp_template = models.ForeignKey("babtynoemail.RSVPEmail",
        on_delete = models.PROTECT,
        blank=True,
        null=True,
    )

    category = models.CharField(max_length=20, null=True, blank=True)
    save_the_date_sent = models.DateTimeField(null=True, blank=True, default=None)
    save_the_date_opened = models.DateTimeField(null=True, blank=True, default=None)
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid, unique=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    is_invited = models.BooleanField(default=False)
    rehearsal_dinner = models.BooleanField(default=False)
    is_attending = models.BooleanField(default=None, null=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited', 'name')

    @property
    def guest_set(self):
        return Guest.objects.filter(party=self)

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(filter(None, self.guest_set.values_list('email', flat=True)))

    class Meta:
        verbose_name_plural = _("Parties")

MEALS = [
    ('beef', 'cow'),
    ('fish', 'fish'),
    ('hen', 'hen'),
    ('vegetarian', 'vegetable'),
]

COURSES = [
    ('app',pg_('In context of menu','Appetiser')),
    ('starter',pg_('In context of menu','Starter')),
    ('main',pg_('In context of menu','Main')),
    ('dessert',pg_('In context of menu','Dessert')),
]

class Menu(ClusterableModel):
    name = models.TextField(help_text=_("Vegan? Gluten-free? For Anglophones? For non-Anglophones?"))

    def ordered_dishes(self):
        #Return dishes in order of serving... necessary for views.
        COURSES_ORDER = (course[0] for course in COURSES)
        order = dict((key,idx) for idx,key in enumerate(COURSES_ORDER))
        #return order
        return sorted(self.dish.all(), key=lambda x:order[x.type])

    def __str__(self):
        return "{}".format(self.name)

@register_snippet
class Dish(index.Indexed,TranslatableMixin,Orderable):
    menu = ParentalKey('Menu',on_delete=models.PROTECT,related_name="dish")
    type = models.CharField(max_length=20,choices=COURSES,null=True,blank=True)
    title = models.TextField(help_text=_("Name of the dish"))
    description = models.TextField(help_text=_("Description of the dish"),blank=True,null=True)
    comments = models.TextField(help_text=_("Say if it's vegan, veggie, gluten-free, halal, kosher, etc."),blank=True,null=True)

    panels = [
        # FieldPanel('locale'),
        FieldPanel('type'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('comments'),
    ]

    search_fields = [index.SearchField('title',partial_match=True),]

    def __str__(self):
        return "{} {}".format(self.get_type_display(),self.title)

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = _("Dishes")

STARTERS = [(str(dish.pk),dish.title) for dish in Dish.objects.all() if dish.type=="starter"]
MAINS = [(str(dish.pk),dish.title) for dish in Dish.objects.all() if dish.type=="main"]
DESSERTS = [(str(dish.pk),dish.title) for dish in Dish.objects.all() if dish.type=="dessert"]

class Guest(Orderable):
    """
    A single guest
    """
    party = ParentalKey('Party', on_delete=models.PROTECT,related_name='guests')
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.BooleanField(default=None, null=True)
    is_child = models.BooleanField(default=False)
    starter = models.CharField(max_length=100,null=True,blank=True,choices=STARTERS)
    main = models.CharField(max_length=100,null=True,blank=True,choices=MAINS)
    dessert = models.CharField(max_length=100,null=True,blank=True,choices=DESSERTS)
    #dishes = ParentalManyToManyField("Dish",related_name="dishes",null=True,blank=True)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
