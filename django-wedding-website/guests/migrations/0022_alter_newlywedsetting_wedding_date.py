# Generated by Django 4.1 on 2022-12-26 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0021_newlywedsetting_emailsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newlywedsetting',
            name='wedding_date',
            field=models.DateField(null=True),
        ),
    ]