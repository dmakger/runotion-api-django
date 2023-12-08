# Generated by Django 4.2.7 on 2023-11-23 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userprofile_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='user/images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='ФИО'),
        ),
    ]