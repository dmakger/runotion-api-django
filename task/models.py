from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models import ImportanceLevel
from project.models import Project, SectionProject
from service.position import get_new_position, fix_positions
from user.models import UserProfile


# ===============
#     Задачи
# ==============
class Task(models.Model):
    director = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Постановщик')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    name = models.CharField('Название', max_length=128)
    code = models.CharField('Код', max_length=128)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    deadline = models.DateTimeField('Крайний срок', null=True, default=None, blank=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, default=None, blank=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Task, self).save(*args, **kwargs)
        if created:
            responsible_task = UserLevelTask.objects.get(name='Ответственный')
            UserToTask.objects.create(user=self.director, task=self, position=responsible_task)


# ========================
#     Задачи к Секции
# ========================
class TaskToSection(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    section_project = models.ForeignKey(SectionProject, on_delete=models.CASCADE, verbose_name='Этап в проекте',
                                        null=True, blank=True, default=None)
    created_at = models.DateTimeField('Дата добавления в секцию', auto_now_add=True)
    position = models.IntegerField('Позиция', default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Задача к Секции"
        verbose_name_plural = "Задачи к Секциям"

    def __str__(self):
        return f'{self.task} ==> _проект_ {self.section_project}'


@receiver(post_save, sender=TaskToSection)
def task_to_section_on_create_update(sender, instance, created, **kwargs):
    if created:
        sections = TaskToSection.objects.filter(task=instance.task).order_by('position')
        instance.position = get_new_position(sections, instance.position)
        instance.save()
        fix_positions(sections)


@receiver(post_delete, sender=TaskToSection)
def task_to_section_on_delete(sender, instance, **kwargs):
    sections = TaskToSection.objects.filter(task=instance.task).order_by('position')
    fix_positions(sections)


# ==========================================
#     Должность пользователя в задачах
# ==========================================
class UserLevelTask(models.Model):
    name = models.CharField('Название', max_length=128)
    level = models.ForeignKey(ImportanceLevel, on_delete=models.CASCADE, verbose_name='Уровень')

    class Meta:
        verbose_name = "Должность пользователя в задачах"
        verbose_name_plural = "Должности пользователя в задачах"

    def __str__(self):
        return self.name


# =============================
#     Пользователь к задаче
# =============================
class UserToTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    level = models.ForeignKey(UserLevelTask, on_delete=models.CASCADE,
                              verbose_name='Должность пользователя в задачах')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь к задаче"
        verbose_name_plural = "Пользователи к задаче"

    def __str__(self):
        return f"{self.task.name} ===> {self.user.name}"


# =============================
#     Комментарии у задачи
# =============================
class CommentTask(models.Model):
    user = models.ForeignKey(UserToTask, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий у задачи"
        verbose_name_plural = "Комментарии у задачи"

    def __str__(self):
        return f"{self.task.name} ===> {self.user.name}"


# =============================
#     Чеклист у задачи
# =============================
class ChecklistTask(models.Model):
    user = models.ForeignKey(UserToTask, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Название', max_length=128)
    position = models.IntegerField('Позиция', default=None, null=True, blank=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, default=None, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Чеклист у задачи"
        verbose_name_plural = "Чеклисты у задачи"

    def __str__(self):
        return f"{self.user.task.name} ===> {self.name}"


@receiver(post_save, sender=ChecklistTask)
def checklist_task_on_create_update(sender, instance, created, **kwargs):
    if created:
        checklists = ChecklistTask.objects.filter(user=instance.user).order_by('position')
        instance.position = get_new_position(checklists, instance.position)
        instance.save()
        fix_positions(checklists)


@receiver(post_delete, sender=ChecklistTask)
def checklist_task_on_delete(sender, instance, **kwargs):
    sections = ChecklistTask.objects.filter(user=instance.user).order_by('position')
    fix_positions(sections)


# =============================
#     Подзадачи у чеклиста
# =============================
class SubtaskChecklist(models.Model):
    checklist = models.ForeignKey(ChecklistTask, on_delete=models.CASCADE, verbose_name='Чеклист')
    name = models.CharField('Название', max_length=128)
    position = models.IntegerField('Позиция', default=None, null=True, blank=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, default=None, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Подзадача в чеклисте"
        verbose_name_plural = "Подзадачи в чеклистах"

    def __str__(self):
        return f"{self.checklist.user.task.name} ==> {self.checklist.name} ===> {self.name}"


@receiver(post_save, sender=SubtaskChecklist)
def subtask_checklist_on_create_update(sender, instance, created, **kwargs):
    if created:
        qs = SubtaskChecklist.objects.filter(checklist=instance.checklist).order_by('position')
        instance.position = get_new_position(qs, instance.position)
        instance.save()
        fix_positions(qs)


@receiver(post_delete, sender=SubtaskChecklist)
def subtask_checklist_on_delete(sender, instance, **kwargs):
    qs = SubtaskChecklist.objects.filter(checklist=instance.checklist).order_by('position')
    fix_positions(qs)
