from task.models import UserLevelTask


def get_director_task():
    return UserLevelTask.objects.get(id=1)


def get_responsible_task():
    return UserLevelTask.objects.get(id=2)


def get_collaborator_task():
    return UserLevelTask.objects.get(id=3)


def get_observer_task():
    return UserLevelTask.objects.get(id=4)
