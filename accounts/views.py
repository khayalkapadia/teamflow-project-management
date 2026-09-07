from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash


User = get_user_model()


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Username already exists."}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")


def logout_view(request):

    logout(request)

    return redirect("login")


@login_required
def profile(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()

        if not username:

            return render(
                request,
                "accounts/profile.html",
                {
                    "error": "Username is required."
                }
            )

        if User.objects.filter(
            username=username
        ).exclude(
            id=request.user.id
        ).exists():

            return render(
                request,
                "accounts/profile.html",
                {
                    "error": "Username already exists."
                }
            )

        request.user.username = username
        request.user.email = email

        request.user.save()

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html"
    )

@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):

            return render(
                request,
                "accounts/change_password.html",
                {
                    "error": "Current password is incorrect."
                }
            )

        if new_password != confirm_password:

            return render(
                request,
                "accounts/change_password.html",
                {
                    "error": "New passwords do not match."
                }
            )

        if not new_password:

            return render(
                request,
                "accounts/change_password.html",
                {
                    "error": "New password is required."
                }
            )

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(
            request,
            request.user
        )

        return redirect("profile")

    return render(
        request,
        "accounts/change_password.html"
    )