# Generated by Django 4.1 on 2022-11-27 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babtynoemail', '0005_savethedateemail_font_colour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='savethedateemail',
            name='language',
            field=models.CharField(choices=[('en-gb', 'English'), ('lt', 'Lithuanian')], default=('en-gb', 'English'), max_length=25),
        ),
    ]