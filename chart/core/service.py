from project.models import Project
from service.list import get_records_from_model, get_records_from_queryset, get_parents_records
from task.models import UserLevelTask, UserToTask, Task
from task.service import get_director_task
from user.models import UserProfile


def get_projects(request):
    projects = request.data.get('projects', [])
    current_user = UserProfile.objects.get(user=request.user)

    projects_qs = Project.objects.filter(admin=current_user)
    if projects:
        return projects_qs.filter(id__in=projects)
    return projects_qs


def get_tasks(projects, request):
    users_id = request.data.get('users', [])
    levels_id = request.data.get('levels', [])
    qs_tasks = Task.objects.all()

    task_to_project_qs = qs_tasks.filter(project__in=projects)
    levels_qs = get_records_from_model(UserLevelTask, {'id__in': levels_id})
    user_to_task_qs = get_records_from_model(UserToTask, {
        'task__in': task_to_project_qs,
        'user__id__in': users_id,
        'level__in': levels_qs,
    })

    tasks = get_parents_records(user_to_task_qs, Task, ['task'])
    director_level_task = get_director_task()
    if director_level_task not in levels_qs:
        return tasks

    director_tasks = get_records_from_queryset(task_to_project_qs, {'director__in': users_id})
    return tasks.union(director_tasks)
