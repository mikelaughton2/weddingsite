# Generated by Django 4.1 on 2022-11-12 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('babtyno', '0002_rename_body_homepage_hero_text_homepage_about_venue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='hero_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
