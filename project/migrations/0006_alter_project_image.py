# Generated by Django 4.2.7 on 2023-11-03 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_project_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='project/images/', verbose_name='Изображение'),
        ),
    ]