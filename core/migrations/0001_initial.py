# Generated by Django 4.2.7 on 2023-11-02 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportanceLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('value', models.IntegerField(verbose_name='Степень важности')),
            ],
            options={
                'verbose_name': 'Уровень важности',
                'verbose_name_plural': 'Уровни важности',
            },
        ),
    ]
