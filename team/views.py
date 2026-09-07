from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projects.models import Project


@login_required
def team_list(request):

    projects = Project.objects.filter(
        owner=request.user
    ).prefetch_related(
        "members__user"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "team/team_list.html",
        {
            "projects": projects
        }
    )