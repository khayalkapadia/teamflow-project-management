import calendar
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tasks.models import Task


@login_required
def calendar_view(request):

    today = date.today()

    try:
        month = int(
            request.GET.get(
                "month",
                today.month
            )
        )

        year = int(
            request.GET.get(
                "year",
                today.year
            )
        )

    except (ValueError, TypeError):

        month = today.month
        year = today.year


    # Make sure the month is valid

    if month < 1:

        month = 12
        year -= 1


    if month > 12:

        month = 1
        year += 1


    # Create calendar

    current_calendar = calendar.Calendar(
        firstweekday=0
    )

    weeks = current_calendar.monthdayscalendar(
        year,
        month
    )


    # Get the user's tasks for this month

    tasks = Task.objects.filter(
        assigned_to=request.user,
        due_date__year=year,
        due_date__month=month
    ).select_related(
        "project"
    ).order_by(
        "due_date",
        "priority",
        "created_at"
    )


    # Organize tasks by day

    tasks_by_day = {}

    for task in tasks:

        day = task.due_date.day

        if day not in tasks_by_day:

            tasks_by_day[day] = []

        tasks_by_day[day].append(task)


    # Previous month

    previous_month = month - 1
    previous_year = year

    if previous_month == 0:

        previous_month = 12
        previous_year -= 1


    # Next month

    next_month = month + 1
    next_year = year

    if next_month == 13:

        next_month = 1
        next_year += 1


    # Check whether this is the current month

    is_current_month = (
        month == today.month
        and year == today.year
    )


    # Count tasks

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status="done"
    ).count()

    pending_tasks = tasks.exclude(
        status="done"
    ).count()


    return render(
        request,
        "calendar/calendar.html",
        {
            "weeks": weeks,

            "month_name": calendar.month_name[month],

            "month": month,

            "year": year,

            "tasks_by_day": tasks_by_day,

            "previous_month": previous_month,

            "previous_year": previous_year,

            "next_month": next_month,

            "next_year": next_year,

            "today": today,

            "is_current_month": is_current_month,

            "total_tasks": total_tasks,

            "completed_tasks": completed_tasks,

            "pending_tasks": pending_tasks,
        }
    )