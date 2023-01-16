# Generated by Django 4.1 on 2023-01-14 23:43

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0031_remove_dish_guest_guest_dishes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='dishes',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, null=True, related_name='dish', to='guests.dish'),
        ),
    ]