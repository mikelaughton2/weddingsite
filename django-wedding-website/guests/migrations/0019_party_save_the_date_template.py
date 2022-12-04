# Generated by Django 4.1 on 2022-11-27 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('babtynoemail', '0006_savethedateemail_language'),
        ('guests', '0018_alter_party_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='save_the_date_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='babtynoemail.savethedateemail'),
        ),
    ]
