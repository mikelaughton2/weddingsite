from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from wagtail.models import Orderable,ClusterableModel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.admin.panels import ObjectList
from modelcluster.fields import ParentalKey


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
    def guest__set(self):
        return Guest.objects.filter(party=self)

    @property
    def ordered_guests(self):
        return self.guest__set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest__set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(filter(None, self.guest__set.values_list('email', flat=True)))

    class Meta:
        verbose_name_plural = "Parties"

MEALS = [
    ('beef', 'cow'),
    ('fish', 'fish'),
    ('hen', 'hen'),
    ('vegetarian', 'vegetable'),
]


class Guest(Orderable):
    """
    A single guest
    """
    party = ParentalKey('Party', on_delete=models.CASCADE,related_name='guests')
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.BooleanField(default=None, null=True)
    meal = models.CharField(max_length=20, choices=MEALS, null=True, blank=True)
    is_child = models.BooleanField(default=False)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
