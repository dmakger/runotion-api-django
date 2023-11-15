from project.models import Project
from task.models import Task


def get_new_code_task_by_project(project: Project):
    len_tasks = len(Task.objects.filter(project=project))
    return f"{project.code}-{len_tasks+1}"
