# Generated by Django 2.2 on 2019-06-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0002_auto_20190625_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='photo',
            field=models.ImageField(blank=True, upload_to='profile_photo'),
        ),
    ]
