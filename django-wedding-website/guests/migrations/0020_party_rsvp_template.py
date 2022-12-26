# Generated by Django 4.1 on 2022-12-10 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('babtynoemail', '0007_rsvpemail'),
        ('guests', '0019_party_save_the_date_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='rsvp_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='babtynoemail.rsvpemail'),
        ),
    ]