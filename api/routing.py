from django.urls import path

from task.consumers import NotificationConsumer, TaskCommentConsumer


websocket_urlpatterns = [
    path('ws/tasks/<int:task_id>/comments/', TaskCommentConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]
