# Generated by Django 2.2 on 2019-07-12 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0007_posts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
        migrations.CreateModel(
            name='TimeLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perfil', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_timeline', to='perfis.Perfil')),
            ],
        ),
    ]
