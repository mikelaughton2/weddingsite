# Generated by Django 4.1 on 2022-12-26 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('guests', '0020_party_rsvp_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewlyWedSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newlyweds', models.CharField(max_length=150)),
                ('wedding_date', models.DateField()),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_wedding_email', models.EmailField(max_length=254)),
                ('default_wedding_from_email', models.EmailField(max_length=254)),
                ('default_wedding_reply_email', models.EmailField(max_length=254)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
