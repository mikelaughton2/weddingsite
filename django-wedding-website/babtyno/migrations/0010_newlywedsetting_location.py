# Generated by Django 4.1 on 2022-12-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babtyno', '0009_newlywedsetting_emailsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='newlywedsetting',
            name='location',
            field=models.CharField(default='TBD!', max_length=150),
        ),
    ]
