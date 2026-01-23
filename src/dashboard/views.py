from django.shortcuts import render
from django.http import HttpResponse
from accounts.views import is_admin,get_role_level
from conditions.models import Condition
from django.utils import timezone
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
import json
from analysis.utils import load_opinion_csv, count_by_tag
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "dashboard/index.html")

#管理者用画面
def dashboard_home(request):
    if not is_admin(request.user):
        return render(request, "dashboard/forbidden.html")
    #管理者レベル取得/レベル判定
    role = get_role_level(request.user)
    show_name = True
    if role == 2:
        # 表示制御
        show_name = False
    #期間フィルタ（今日 / 今月）
    period = request.GET.get("period", "today")
    today = timezone.localdate()
    #部署別集計
    dept_stats = (
        Condition.objects
        .filter(is_absent=False)
        .values("user__employeeprofile__department")
        .annotate(
            avg_physical=Avg("physical"),
            avg_mental=Avg("mental"),
        )
        .order_by("user__employeeprofile__department")
    )
    #月次集計
    monthly_stats = (
        Condition.objects
        .filter(is_absent=False)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            avg_physical=Avg("physical"),
            avg_mental=Avg("mental"),
            count=Count("id"),
        )
        .order_by("month")
    )
    #csv読み込み
    csv_path = os.path.join(
        settings.BASE_DIR.parent,
        "php_opinion_box",
        "opinions",
        "opinion_box.csv",
    )
    opinion_df = load_opinion_csv(csv_path)
    # CSV集計（安全版）
    try:
        opinion_df = load_opinion_csv(csv_path)
        tag_counts = count_by_tag(opinion_df)
    except Exception:
        tag_counts = {}

    #conditionグラフ表示用jsonデータ作成
    months_json = json.dumps([
        row["month"].strftime("%Y-%m") for row in monthly_stats
    ])
    avg_physical_json = json.dumps([
        row["avg_physical"] for row in monthly_stats
    ])
    avg_mental_json = json.dumps([
        row["avg_mental"] for row in monthly_stats
    ])

    #集計クエリを期間で分岐
    qs = Condition.objects.all()

    if period == "month":
        qs = qs.filter(date__year=today.year, date__month=today.month)
    else:
        qs = qs.filter(date=today)

    total_count = qs.count()
    absent_count = qs.filter(is_absent=True).count()
    present_count = qs.filter(is_absent=False).count()

    return render(
        request,
        "dashboard/home.html",
        {
            "role_level": role,
            "period": period,
            "show_name": show_name,
            "dept_stats": dept_stats,
            "monthly_stats": monthly_stats,
            "months_json": months_json,
            "avg_physical_json": avg_physical_json,
            "avg_mental_json": avg_mental_json,
            "tag_counts": tag_counts,
            "total_count": total_count,
            "absent_count": absent_count,
            "present_count": present_count,
        }
    )

