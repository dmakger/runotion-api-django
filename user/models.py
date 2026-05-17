from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# ====================
#     Департамент
# ====================
class Department(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

    def __str__(self):
        return self.name


# =============================
#   Расширенные пользователи
# =============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('ФИО', max_length=100, null=True, blank=True, default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Департамент', null=True, blank=True, default=None)
    image = models.ImageField('Изображение', upload_to='user/images/', null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Расширенный пользователь"
        verbose_name_plural = "Расширенные пользователи"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class RegistrationRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_APPROVED, 'Принята'),
        (STATUS_REJECTED, 'Отклонена'),
    )

    mts_login = models.CharField('Логин МТС', max_length=150, blank=True, default='')
    username = models.CharField('Логин', max_length=150, blank=True, default='')
    password = models.CharField('Пароль', max_length=128, blank=True, default='')
    full_name = models.CharField('ФИО', max_length=150, blank=True, default='')
    comment = models.TextField('Комментарий', blank=True, default='')
    status = models.CharField('Статус', max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                     verbose_name='Созданный пользователь')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрацию'

    def __str__(self):
        return self.mts_login or self.username or f'Заявка #{self.pk}'
