from django.urls import path

from . import views


urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("create/", views.create_project, name="create_project"),
    path("<int:project_id>/", views.project_detail, name="project_detail"),
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("<int:project_id>/delete/", views.delete_project, name="delete_project"),
    path("<int:project_id>/members/", views.project_members, name="project_members"),
    path("<int:project_id>/members/<int:member_id>/edit/", views.edit_member, name="edit_member"),
    path("<int:project_id>/members/<int:member_id>/remove/", views.remove_member, name="remove_member"),
]