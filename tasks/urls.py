from django.urls import path

from . import views


urlpatterns = [
    path("<int:project_id>/", views.task_board, name="task_board"),
    path("<int:project_id>/create/", views.create_task, name="create_task"),
    path("<int:project_id>/<int:task_id>/", views.task_detail, name="task_detail"),
    path("<int:project_id>/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("<int:project_id>/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("my-tasks/", views.my_tasks, name="my_tasks")
]