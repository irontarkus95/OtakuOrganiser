# Generated by Django 2.0.4 on 2018-04-09 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OtakuOrganiserApp', '0005_auto_20180409_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='anime_photo',
            field=models.ImageField(default='img/placeholder.jpg', null=True, upload_to='img/profiles', verbose_name='Anime Photo'),
        ),
    ]
