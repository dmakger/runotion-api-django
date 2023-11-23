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
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Департамент')
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
