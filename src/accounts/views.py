from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView

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

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        user = self.request.user

        # role_level を使う（設計書準拠）
        role_level = get_role_level(user)

        # 管理者 → ダッシュボード
        if role_level >= 1:
            return "/dashboard/"

        # 一般ユーザー → 体調入力
        return "/conditions/"

