from django.shortcuts import render
from django.http import HttpResponse
from accounts.views import is_admin,get_role_level
from conditions.models import Condition
from django.utils import timezone

def dashboard_home(request):
    if not is_admin(request.user):
        return render(request, "dashboard/forbidden.html")

    role = get_role_level(request.user)
    today = timezone.localdate()

    total_count = Condition.objects.filter(date=today).count()
    absent_count = Condition.objects.filter(date=today, is_absent=True).count()
    present_count = Condition.objects.filter(date=today, is_absent=False).count()

    return render(
        request,
        "dashboard/home.html",
        {
            "role_level": role,
            "total_count": total_count,
            "absent_count": absent_count,
            "present_count": present_count,
        }
    )

