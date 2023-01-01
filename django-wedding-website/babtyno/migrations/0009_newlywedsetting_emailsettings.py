# Generated by Django 4.1 on 2022-12-26 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('babtyno', '0008_blogpost_rsvp_simplepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewlyWedSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newlyweds', models.CharField(default='Happy & Couple', max_length=150)),
                ('wedding_date', models.DateField(null=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Newlywed Setting',
            },
        ),
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_wedding_email', models.EmailField(default='example@example.com', max_length=254)),
                ('default_wedding_from_email', models.EmailField(default='example@example.com', max_length=254)),
                ('default_wedding_reply_email', models.EmailField(default='example@example.com', max_length=254)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Email settings',
            },
        ),
    ]
