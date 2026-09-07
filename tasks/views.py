from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from projects.models import Project
from .models import Task, TaskActivity, TaskComment
from notifications.models import Notification


@login_required
def task_board(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    todo_tasks = Task.objects.filter(
        project=project,
        status="todo"
    ).order_by(
        "due_date",
        "-created_at"
    )

    progress_tasks = Task.objects.filter(
        project=project,
        status="in_progress"
    ).order_by(
        "due_date",
        "-created_at"
    )

    done_tasks = Task.objects.filter(
        project=project,
        status="done"
    ).order_by(
        "due_date",
        "-created_at"
    )

    today = date.today()

    return render(
        request,
        "tasks/task_board.html",
        {
            "project": project,
            "todo_tasks": todo_tasks,
            "progress_tasks": progress_tasks,
            "done_tasks": done_tasks,
            "todo_count": todo_tasks.count(),
            "progress_count": progress_tasks.count(),
            "done_count": done_tasks.count(),
            "today": today
        }
    )


@login_required
def create_task(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    members = project.members.select_related("user")

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        assigned_to_id = request.POST.get("assigned_to")
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date") or None

        if not title:

            return render(
                request,
                "tasks/create_task.html",
                {
                    "project": project,
                    "members": members,
                    "error": "Task title is required."
                }
            )

        assigned_to = None

        if assigned_to_id:

            member = get_object_or_404(
                project.members.select_related("user"),
                user_id=assigned_to_id
            )

            assigned_to = member.user

        task = Task.objects.create(
            title=title,
            description=description,
            project=project,
            assigned_to=assigned_to,
            created_by=request.user,
            status=status,
            priority=priority,
            due_date=due_date
        )

        TaskActivity.objects.create(
            task=task,
            user=request.user,
            action="created this task"
        )

        if assigned_to:

            TaskActivity.objects.create(
                task=task,
                user=request.user,
                action=f"assigned this task to {assigned_to.username}"
            )

        if assigned_to and assigned_to != request.user:

            Notification.objects.create(
                recipient=assigned_to,
                message=f'You have been assigned a new task: "{task.title}"',
                link=f"/tasks/{project.id}/{task.id}/"
            )

        return redirect(
            "task_board",
            project_id=project.id
        )

    return render(
        request,
        "tasks/create_task.html",
        {
            "project": project,
            "members": members
        }
    )


@login_required
def task_detail(request, project_id, task_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    is_owner = project.owner == request.user

    is_member = project.members.filter(
        user=request.user
    ).exists()

    if not is_owner and not is_member:

        return redirect("dashboard")

    task = get_object_or_404(
        Task,
        id=task_id,
        project=project
    )

    if request.method == "POST":

        content = request.POST.get(
            "comment",
            ""
        ).strip()

        if content:

            TaskComment.objects.create(
                task=task,
                user=request.user,
                content=content
            )

            TaskActivity.objects.create(
                task=task,
                user=request.user,
                action="added a comment"
            )

        return redirect(
            "task_detail",
            project_id=project.id,
            task_id=task.id
        )

    comments = task.comments.select_related(
        "user"
    ).order_by(
        "created_at"
    )

    activities = task.activities.select_related(
        "user"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "tasks/task_detail.html",
        {
            "project": project,
            "task": task,
            "comments": comments,
            "activities": activities
        }
    )


@login_required
def edit_task(request, project_id, task_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    is_owner = project.owner == request.user

    member = project.members.filter(
        user=request.user
    ).first()

    is_member = member is not None

    if not is_owner and not is_member:

        return redirect("dashboard")

    task = get_object_or_404(
        Task,
        id=task_id,
        project=project
    )

    if is_owner or (
        member and member.role == "manager"
    ):

        members = project.members.select_related(
            "user"
        )

        if request.method == "POST":

            title = request.POST.get("title")
            description = request.POST.get("description")
            assigned_to_id = request.POST.get("assigned_to")
            status = request.POST.get("status")
            priority = request.POST.get("priority")
            due_date = request.POST.get("due_date") or None

            if not title:

                return render(
                    request,
                    "tasks/edit_task.html",
                    {
                        "project": project,
                        "task": task,
                        "members": members,
                        "error": "Task title is required."
                    }
                )

            assigned_to = None

            if assigned_to_id:

                assigned_member = get_object_or_404(
                    project.members.select_related("user"),
                    user_id=assigned_to_id
                )

                assigned_to = assigned_member.user

            old_status = task.status

            task.title = title
            task.description = description
            task.assigned_to = assigned_to
            task.status = status
            task.priority = priority
            task.due_date = due_date

            task.save()

            if old_status != task.status:

                TaskActivity.objects.create(
                    task=task,
                    user=request.user,
                    action=f"changed the status to {task.get_status_display()}"
                )

            return redirect(
                "task_detail",
                project_id=project.id,
                task_id=task.id
            )

        return render(
            request,
            "tasks/edit_task.html",
            {
                "project": project,
                "task": task,
                "members": members
            }
        )

    if member and member.role in [
        "developer",
        "designer"
    ]:

        if task.assigned_to != request.user:

            return redirect(
                "task_detail",
                project_id=project.id,
                task_id=task.id
            )

        if request.method == "POST":

            new_status = request.POST.get(
                "status"
            )

            if new_status not in [
                "todo",
                "in_progress",
                "done"
            ]:

                return redirect(
                    "task_detail",
                    project_id=project.id,
                    task_id=task.id
                )

            old_status = task.status

            task.status = new_status

            task.save()

            if old_status != new_status:

                TaskActivity.objects.create(
                    task=task,
                    user=request.user,
                    action=f"changed the status to {task.get_status_display()}"
                )

            return redirect(
                "task_detail",
                project_id=project.id,
                task_id=task.id
            )

        return render(
            request,
            "tasks/edit_task.html",
            {
                "project": project,
                "task": task,
                "status_only": True
            }
        )

    return redirect(
        "task_detail",
        project_id=project.id,
        task_id=task.id
    )

@login_required
def delete_task(request, project_id, task_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    task = get_object_or_404(
        Task,
        id=task_id,
        project=project
    )

    can_delete = (
        project.owner == request.user
        or task.created_by == request.user
    )

    if not can_delete:
        return redirect(
            "task_detail",
            project_id=project.id,
            task_id=task.id
        )

    if request.method == "POST":

        task.delete()

        return redirect(
            "task_board",
            project_id=project.id
        )

    return render(
        request,
        "tasks/delete_task.html",
        {
            "project": project,
            "task": task
        }
    )

@login_required
def my_tasks(request):

    tasks = Task.objects.filter(
        assigned_to=request.user
    ).select_related(
        "project"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status_filter = request.GET.get(
        "status",
        ""
    ).strip()

    if search:

        tasks = tasks.filter(
            title__icontains=search
        )

    if status_filter in [
        "todo",
        "in_progress",
        "done"
    ]:

        tasks = tasks.filter(
            status=status_filter
        )

    tasks = tasks.order_by(
        "status",
        "due_date",
        "-created_at"
    )

    today = date.today()

    total_count = Task.objects.filter(
        assigned_to=request.user
    ).count()

    in_progress_count = Task.objects.filter(
        assigned_to=request.user,
        status="in_progress"
    ).count()

    completed_count = Task.objects.filter(
        assigned_to=request.user,
        status="done"
    ).count()

    overdue_count = Task.objects.filter(
        assigned_to=request.user,
        due_date__lt=today
    ).exclude(
        status="done"
    ).count()

    return render(
        request,
        "tasks/my_tasks.html",
        {
            "tasks": tasks,
            "total_count": total_count,
            "in_progress_count": in_progress_count,
            "completed_count": completed_count,
            "overdue_count": overdue_count,
            "today": today,
            "search": search,
            "status_filter": status_filter,
        }
    )