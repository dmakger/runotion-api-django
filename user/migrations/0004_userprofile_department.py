# Generated by Django 4.2.7 on 2023-11-23 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_userprofile_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.department', verbose_name='Департамент'),
            preserve_default=False,
        ),
    ]