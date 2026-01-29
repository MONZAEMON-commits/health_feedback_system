from django.shortcuts import render
from accounts.views import is_admin, get_role_level
from conditions.models import Condition
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from analysis.services import build_analysis_dataframes
import os


@login_required
def index(request):
    return render(request, "dashboard/index.html")

def dashboard_home(request):
    if not is_admin(request.user):
        return render(request, "dashboard/forbidden.html")

    # 管理者レベル
    role = get_role_level(request.user)
    show_name = False if role == 2 else True

    # 期間フィルタ（今日 / 今月）
    period = request.GET.get("period", "today")
    today = timezone.localdate()

    qs = Condition.objects.all()
    if period == "month":
        qs = qs.filter(date__year=today.year, date__month=today.month)
    else:
        qs = qs.filter(date=today)

    total_count = qs.count()
    absent_count = qs.filter(is_absent=True).count()
    present_count = qs.filter(is_absent=False).count()

    # CSV パス
    csv_path = os.path.join(
        settings.BASE_DIR.parent,
        "php_opinion_box",
        "opinions",
        "opinion_box.csv",
    )

    # analysis 実行
    analysis_data = build_analysis_dataframes(csv_path)
    condition_stats = analysis_data.get("condition_stats")

    avg_physical = avg_mental = None
    median_physical = median_mental = None

    if condition_stats is not None and not condition_stats.empty:
        physical = condition_stats[condition_stats["metric"] == "physical"]
        mental = condition_stats[condition_stats["metric"] == "mental"]

        if not physical.empty:
            avg_physical = physical["mean"].iloc[0]
            median_physical = physical["median"].iloc[0]

        if not mental.empty:
            avg_mental = mental["mean"].iloc[0]
            median_mental = mental["median"].iloc[0]

    return render(
        request,
        "dashboard/home.html",
        {
            "role_level": role,
            "period": period,
            "show_name": show_name,
            "total_count": total_count,
            "absent_count": absent_count,
            "present_count": present_count,
            "avg_physical_analysis": avg_physical,
            "avg_mental_analysis": avg_mental,
            "median_physical_analysis": median_physical,
            "median_mental_analysis": median_mental,
        }
    )
