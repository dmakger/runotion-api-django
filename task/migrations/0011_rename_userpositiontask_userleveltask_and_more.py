# Generated by Django 4.2.7 on 2023-11-16 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('task', '0010_rename_userpositiontasktotask_usertotask'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPositionTask',
            new_name='UserLevelTask',
        ),
        migrations.RenameField(
            model_name='usertotask',
            old_name='position',
            new_name='level',
        ),
    ]