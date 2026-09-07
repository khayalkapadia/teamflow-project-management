from django.conf import settings
from django.db import models


class Project(models.Model):

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

class ProjectMember(models.Model):

    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("developer", "Developer"),
        ("designer", "Designer"),
        ("viewer", "Viewer"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="developer"
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"