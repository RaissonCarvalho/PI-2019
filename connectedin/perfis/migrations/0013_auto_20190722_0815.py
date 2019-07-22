# Generated by Django 2.2 on 2019-07-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0012_auto_20190722_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='contatos',
            field=models.ManyToManyField(related_name='meus_contatos', to='perfis.Perfil'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='photo',
            field=models.ImageField(blank=True, default='default_photo.png', upload_to='profile_photo'),
        ),
    ]