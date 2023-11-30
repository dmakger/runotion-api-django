from django.db import models
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from core.models import ImportanceLevel
from service.position import fix_positions, get_new_position
from user.models import UserProfile


# ===============
#     Проект
# ==============
class Project(models.Model):
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Админ')
    name = models.CharField('Название', max_length=128)
    code = models.CharField('Код', max_length=128)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='project/images/', null=True, default=None, blank=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


@receiver(post_save, sender=Project)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SectionProject.objects.create(project=instance, name='Новые')
        SectionProject.objects.create(project=instance, name='В процессе')
        SectionProject.objects.create(project=instance, name='Выполненные')


# ===================
#   Роль в проекте
# ===================
class RoleProject(models.Model):
    name = models.CharField('Название', max_length=128)
    level = models.OneToOneField(ImportanceLevel, on_delete=models.CASCADE, verbose_name='Уровень')

    class Meta:
        verbose_name = "Роль в проекте"
        verbose_name_plural = "Роли в проекте"

    def __str__(self):
        return self.name


# ==============================
#     Пользователь к проекту
# =============================
class UserToProject(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    role = models.ForeignKey(RoleProject, on_delete=models.CASCADE, verbose_name='Роль')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь к проекту"
        verbose_name_plural = "Пользователь к проектам"

    def __str__(self):
        return f'{self.project} {self.user} {self.role}'


# ===============================
#   Этапы в проекте (Канбан)
# ===============================
class SectionProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    name = models.CharField('Название', max_length=128)
    position = models.IntegerField('Позиция', default=None, null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Этапы проекта"
        verbose_name_plural = "Этапы проектов"

    def __str__(self):
        return f"{self.project.name} ===> {self.name}"


@receiver(post_save, sender=SectionProject)
def section_project_on_create_update(sender, instance, created, **kwargs):
    if created:
        qs = SectionProject.objects.filter(project=instance.project).order_by('position')
        instance.position = get_new_position(qs, instance.position)
        instance.save()
        fix_positions(qs)


@receiver(post_delete, sender=SectionProject)
def section_project_on_delete(sender, instance, **kwargs):
    qs = SectionProject.objects.filter(project=instance.project).order_by('position')
    fix_positions(qs)


# =========================
#   Активность в проекте
# =========================
class ActionProject(models.Model):
    name = models.CharField('Название', max_length=128)

    class Meta:
        verbose_name = "Активность проекта"
        verbose_name_plural = "Активности проектов"

    def __str__(self):
        return self.name


# ======================
#   История проекта
# ======================
class HistoryProject(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='history_projects_created')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    action = models.ForeignKey(ActionProject, on_delete=models.CASCADE, verbose_name='Активность')
    victim = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Жертва',
                               related_name='history_projects_affected')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "История проекта"
        verbose_name_plural = "История проекта"

    def __str__(self):
        return f"{self.project.name} ===> {self.user.name}"
