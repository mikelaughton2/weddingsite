# Generated by Django 4.1 on 2023-01-14 18:16

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0025_menu_alter_guest_party_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the dish', null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='menu',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.PROTECT, related_name='dish', to='guests.menu'),
        ),
    ]