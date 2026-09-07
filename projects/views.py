from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import Project, ProjectMember


User = get_user_model()


@login_required
def project_list(request):

    projects = Project.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects
        }
    )


@login_required
def create_project(request):

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date") or None
        due_date = request.POST.get("due_date") or None
        status = request.POST.get("status")
        priority = request.POST.get("priority")

        if not name:

            return render(
                request,
                "projects/create_project.html",
                {
                    "error": "Project name is required."
                }
            )

        if start_date and due_date and due_date < start_date:

            return render(
                request,
                "projects/create_project.html",
                {
                    "error": "Due date cannot be before the start date."
                }
            )

        Project.objects.create(
            name=name,
            description=description,
            owner=request.user,
            start_date=start_date,
            due_date=due_date,
            status=status,
            priority=priority
        )

        return redirect("project_list")

    return render(
        request,
        "projects/create_project.html"
    )


@login_required
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project
        }
    )


@login_required
def edit_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date") or None
        due_date = request.POST.get("due_date") or None
        status = request.POST.get("status")
        priority = request.POST.get("priority")

        if not name:

            return render(
                request,
                "projects/edit_project.html",
                {
                    "project": project,
                    "error": "Project name is required."
                }
            )

        if start_date and due_date and due_date < start_date:

            return render(
                request,
                "projects/edit_project.html",
                {
                    "project": project,
                    "error": "Due date cannot be before the start date."
                }
            )

        project.name = name
        project.description = description
        project.start_date = start_date
        project.due_date = due_date
        project.status = status
        project.priority = priority

        project.save()

        return redirect(
            "project_detail",
            project_id=project.id
        )

    return render(
        request,
        "projects/edit_project.html",
        {
            "project": project
        }
    )


@login_required
def delete_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    if request.method == "POST":

        project.delete()

        return redirect("project_list")

    return render(
        request,
        "projects/delete_project.html",
        {
            "project": project
        }
    )


@login_required
def project_members(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    if request.method == "POST":

        user_id = request.POST.get("user")
        role = request.POST.get("role")

        user = get_object_or_404(
            User,
            id=user_id
        )

        if ProjectMember.objects.filter(
            project=project,
            user=user
        ).exists():

            users = User.objects.exclude(
                id=request.user.id
            )

            members = ProjectMember.objects.filter(
                project=project
            ).select_related("user")

            return render(
                request,
                "projects/members.html",
                {
                    "project": project,
                    "users": users,
                    "members": members,
                    "error": "This user is already a member of this project."
                }
            )

        ProjectMember.objects.create(
            project=project,
            user=user,
            role=role
        )

        return redirect(
            "project_members",
            project_id=project.id
        )

    users = User.objects.exclude(
        id=request.user.id
    )

    members = ProjectMember.objects.filter(
        project=project
    ).select_related("user")

    return render(
        request,
        "projects/members.html",
        {
            "project": project,
            "users": users,
            "members": members
        }
    )


@login_required
def edit_member(request, project_id, member_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    member = get_object_or_404(
        ProjectMember,
        id=member_id,
        project=project
    )

    if request.method == "POST":

        role = request.POST.get("role")

        member.role = role

        member.save()

        return redirect(
            "project_members",
            project_id=project.id
        )

    return render(
        request,
        "projects/edit_member.html",
        {
            "project": project,
            "member": member
        }
    )


@login_required
def remove_member(request, project_id, member_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    member = get_object_or_404(
        ProjectMember,
        id=member_id,
        project=project
    )

    if request.method == "POST":

        member.delete()

        return redirect(
            "project_members",
            project_id=project.id
        )

    return render(
        request,
        "projects/remove_member.html",
        {
            "project": project,
            "member": member
        }
    )