from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from task.models import CommentTask, Notification, Task, UserToTask
from task.notifications import notify_task_participants
from task.serializers import CommentTaskSerializer, NotificationSerializer
from task.service import get_collaborator_task
from task.views.task import can_comment_task, can_view_task
from user.models import UserProfile


class TaskCommentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f'task_comments_{self.task_id}'

        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        can_connect = await self.user_can_view_task()
        if not can_connect:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get('type') != 'comment.create':
            return

        text = (content.get('text') or '').strip()
        if not text:
            await self.send_json({'type': 'error', 'detail': 'text is required'})
            return

        comment = await self.create_comment(text)
        if comment is None:
            await self.send_json({'type': 'error', 'detail': 'Forbidden'})
            return

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'comment.created',
                'comment': comment,
            },
        )

    async def comment_created(self, event):
        await self.send_json({
            'type': 'comment.created',
            'comment': event['comment'],
        })

    async def history_created(self, event):
        await self.send_json({
            'type': 'history.created',
            'history': event['history'],
        })

    @database_sync_to_async
    def user_can_view_task(self):
        task = Task.objects.filter(pk=self.task_id).select_related('director__user', 'project__admin__user').first()
        return task is not None and can_view_task(task, self.scope['user'])

    @database_sync_to_async
    def create_comment(self, text):
        task = Task.objects.filter(pk=self.task_id).select_related('project', 'project__admin').first()
        if task is None or not can_comment_task(task, self.scope['user']):
            return None

        current_user = UserProfile.objects.get(user=self.scope['user'])
        user_to_task = UserToTask.objects.filter(task=task, user=current_user).first()
        if user_to_task is None:
            user_to_task = UserToTask.objects.create(task=task, user=current_user, level=get_collaborator_task())

        comment = CommentTask.objects.create(user=user_to_task, text=text)
        notify_task_participants(
            task=task,
            notification_type='task_comment',
            title=f'Новый комментарий в задаче {task.code}',
            text=task.name,
            actor=current_user,
        )
        return CommentTaskSerializer(comment).data


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.user_profile_id = await self.get_user_profile_id()
        if self.user_profile_id is None:
            await self.close()
            return

        self.group_name = f'notifications_{self.user_profile_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get('type') == 'notifications.read':
            await self.mark_notifications_read(content.get('ids') or [])

    async def notification_created(self, event):
        await self.send_json({
            'type': 'notification.created',
            'notification': event['notification'],
        })

    @database_sync_to_async
    def get_user_profile_id(self):
        profile = UserProfile.objects.filter(user=self.scope['user']).first()
        return profile.id if profile is not None else None

    @database_sync_to_async
    def mark_notifications_read(self, ids):
        Notification.objects.filter(user_id=self.user_profile_id, id__in=ids).update(is_read=True)
