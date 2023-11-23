from task.models import UserLevelTask


def get_responsible_task():
    return UserLevelTask.objects.get(name='Ответственный')


def get_collaborator_task():
    return UserLevelTask.objects.get(name='Соисполнитель')


def get_observer_task():
    return UserLevelTask.objects.get(name='Наблюдатель')
