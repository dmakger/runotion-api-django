# Generated by Django 4.2.7 on 2023-11-03 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('project', '0003_usertoproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='admin',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='Админ'),
        ),
    ]
