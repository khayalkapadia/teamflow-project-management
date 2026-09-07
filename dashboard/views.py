from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):

    today = date.today()
    soon_date = today + timedelta(days=7)

    projects = Project.objects.filter(
        owner=request.user
    )

    my_tasks = Task.objects.filter(
        assigned_to=request.user
    )

    project_count = projects.count()

    my_tasks_count = my_tasks.count()

    completed_count = my_tasks.filter(
        status="done"
    ).count()

    in_progress_count = my_tasks.filter(
        status="in_progress"
    ).count()

    overdue_count = my_tasks.filter(
        due_date__lt=today
    ).exclude(
        status="done"
    ).count()

    due_soon_count = my_tasks.filter(
        due_date__gte=today,
        due_date__lte=soon_date
    ).exclude(
        status="done"
    ).count()

    recent_projects = projects.order_by(
        "-created_at"
    )[:5]

    recent_tasks = my_tasks.select_related(
        "project"
    ).order_by(
        "-created_at"
    )[:5]

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "project_count": project_count,
            "my_tasks_count": my_tasks_count,
            "completed_count": completed_count,
            "in_progress_count": in_progress_count,
            "overdue_count": overdue_count,
            "due_soon_count": due_soon_count,
            "recent_projects": recent_projects,
            "recent_tasks": recent_tasks,
            "today": today,
            "soon_date": soon_date,
        }
    )