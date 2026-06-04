from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_sectionproject_is_final'),
        ('user', '0007_registrationrequest'),
        ('task', '0015_task_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64, verbose_name='Тип')),
                ('title', models.CharField(max_length=180, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, default='', verbose_name='Текст')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='sent_notifications', to='user.userprofile',
                                            verbose_name='Инициатор')),
                ('project', models.ForeignKey(blank=True, default=None, null=True,
                                              on_delete=django.db.models.deletion.CASCADE, to='project.project',
                                              verbose_name='Проект')),
                ('task', models.ForeignKey(blank=True, default=None, null=True,
                                           on_delete=django.db.models.deletion.CASCADE, to='task.task',
                                           verbose_name='Задача')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications',
                                           to='user.userprofile', verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ['-created_at', '-id'],
            },
        ),
    ]
