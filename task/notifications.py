from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from task.models import Notification, UserToTask
from task.serializers import NotificationSerializer


def get_task_participants(task, exclude_user=None):
    users = {item.user for item in UserToTask.objects.filter(task=task).select_related('user', 'user__user')}
    users.add(task.director)
    users.add(task.project.admin)
    if exclude_user is not None:
        users = {user for user in users if user.user_id != exclude_user.id}
    return list(users)


def send_notification(user, notification_type, title, text='', actor=None, project=None, task=None):
    if actor is not None and user.id == actor.id:
        return None

    notification = Notification.objects.create(
        user=user,
        actor=actor,
        project=project,
        task=task,
        type=notification_type,
        title=title,
        text=text,
    )
    payload = NotificationSerializer(notification).data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'notification.created',
            'notification': payload,
        },
    )
    return notification


def notify_task_participants(task, notification_type, title, text='', actor=None):
    for user in get_task_participants(task, exclude_user=actor.user if actor is not None else None):
        send_notification(
            user=user,
            notification_type=notification_type,
            title=title,
            text=text,
            actor=actor,
            project=task.project,
            task=task,
        )
