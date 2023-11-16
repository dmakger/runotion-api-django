from django.db.models import Max

from project.models import Project
from task.models import Task, ChecklistTask, UserToTask


# Получение нового кода для задачи
def get_new_code_task_by_project(project: Project):
    len_tasks = len(Task.objects.filter(project=project))
    return f"{project.code}-{len_tasks + 1}"


# Получение новой позиции для чеклиста у задачи
def get_new_position_checklist_by_user_to_task(user_to_task: UserToTask):
    max_position = ChecklistTask.objects.filter(user=user_to_task).aggregate(Max('position'))['position__max']
    new_position = 1 if max_position is None else max_position + 1
    return new_position
