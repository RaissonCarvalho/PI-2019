# Generated by Django 2.2 on 2019-07-15 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0008_auto_20190712_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='foto',
            field=models.ImageField(blank=True, upload_to='posts_photo'),
        ),
    ]
