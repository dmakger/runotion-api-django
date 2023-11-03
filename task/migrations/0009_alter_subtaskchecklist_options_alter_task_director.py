# Generated by Django 4.2.7 on 2023-11-03 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('task', '0008_alter_checklisttask_completed_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subtaskchecklist',
            options={'verbose_name': 'Подзадача в чеклисте', 'verbose_name_plural': 'Подзадачи в чеклистах'},
        ),
        migrations.AlterField(
            model_name='task',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='Постановщик'),
        ),
    ]
