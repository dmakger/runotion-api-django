from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views.section import SectionProjectDetailAPIView, UpdateTaskSectionProject, AddTaskToSectionProject
from task.views.task import TaskView, DetailTaskView, ChecklistTaskView, ChecklistTaskDeleteAPIView, TaskDeleteAPIView, \
    SubtaskChecklistTaskView, SubtaskChecklistTaskDeleteAPIView, SubtaskChecklistUpdateAPIView, ChecklistUpdateAPIView, \
    TaskUpdateAPIView, TaskCategoryView, TaskUserAPIView, TaskCommentAPIView, NotificationAPIView, \
    TaskAttachmentAPIView, TaskAttachmentDeleteAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Все задачи
    path("all/", TaskView.as_view({'post': 'get_tasks'})),
    path("create/", TaskView.as_view({'post': 'create_task'})),
    path("<int:pk>/update/", TaskUpdateAPIView.as_view()),
    path("project/<int:project_id>/category/", TaskCategoryView.as_view({'get': 'get_categories', 'post': 'create_category'})),
    path("category/<int:pk>/update/", TaskCategoryView.as_view({'put': 'update', 'patch': 'partial_update'})),
    path("category/<int:pk>/delete/", TaskCategoryView.as_view({'delete': 'destroy'})),
    path("notifications/", NotificationAPIView.as_view()),

    # Задачи по секциям
    path("<int:task_id>/add/section/<int:section_project_id>/", AddTaskToSectionProject.as_view()),
    path("section/<int:pk>/", SectionProjectDetailAPIView.as_view()),
    path('section-project/<int:section_project_id>/task/<int:task_id>/update/', UpdateTaskSectionProject.as_view(),
         name='update_task_section_project'),

    # Детальная страница задачи
    path("<int:task_id>/", DetailTaskView.as_view({'get': 'get_detail_task'})),
    path("<int:task_id>/users/", TaskUserAPIView.as_view()),
    path("<int:task_id>/users/<int:user_id>/", TaskUserAPIView.as_view()),
    path("<int:task_id>/comments/", TaskCommentAPIView.as_view()),
    path("<int:task_id>/attachments/", TaskAttachmentAPIView.as_view()),
    path("attachment/<int:pk>/delete/", TaskAttachmentDeleteAPIView.as_view()),
    path("<int:pk>/delete/", TaskDeleteAPIView.as_view()),

    # Чеклист у задачи
    path("<int:task_id>/checklist/", ChecklistTaskView.as_view({'get': 'get_checklists'})),
    path("<int:task_id>/checklist/create/", ChecklistTaskView.as_view({'post': 'create_checklist'})),
    path("checklist/<int:pk>/update/", ChecklistUpdateAPIView.as_view()),
    path("checklist/<int:pk>/delete/", ChecklistTaskDeleteAPIView.as_view()),
    path("checklist/<int:pk>/delete", ChecklistTaskDeleteAPIView.as_view()),

    # Подзадачи у чеклистов
    path("checklist/<int:checklist_id>/subtask/", SubtaskChecklistTaskView.as_view({'get': 'get_subtasks_checklist'})),
    path("checklist/<int:checklist_id>/subtask/create/", SubtaskChecklistTaskView.as_view({'post': 'create_subtask'})),
    path("subtask/<int:pk>/update/", SubtaskChecklistUpdateAPIView.as_view()),
    path("subtask/<int:pk>/delete/", SubtaskChecklistTaskDeleteAPIView.as_view()),

]
