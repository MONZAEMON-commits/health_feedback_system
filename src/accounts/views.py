from django.shortcuts import render
from django.http import HttpResponse

def get_role_level(user):
    try:
        return user.userrole.role_level
    except:
        return 0

def is_admin(user):
    return get_role_level(user) >= 1

def admin_only_view(request):
    if not is_admin(request.user):
        return HttpResponse("権限がありません", status=403)

    return HttpResponse("管理者専用ページ")
