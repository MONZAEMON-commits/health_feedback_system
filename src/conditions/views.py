from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ConditionForm


@login_required
def input_view(request):
    today = date.today()

    if request.method == "POST":
        form = ConditionForm(
            request.POST,
            user=request.user,
            target_date=today
        )
        if form.is_valid():
            condition = form.save(commit=False)
            condition.user = request.user
            condition.date = today  # 当日固定
            condition.save()
            return redirect("conditions_complete")
    else:
        form = ConditionForm(
            user=request.user,
            target_date=today
        )

    return render(
        request,
        "conditions/input.html",
        {
            "form": form,
            "today": today,  # ★ 追加：日付表示用
        }
    )


@login_required
def complete_view(request):
    return render(request, "conditions/complete.html")
