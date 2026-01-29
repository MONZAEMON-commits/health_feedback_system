from django import forms
from datetime import date
from .models import Condition


class ConditionForm(forms.ModelForm):

    class Meta:
        model = Condition
        fields = [
            "physical",
            "mental",
            "is_absent",
            "notes",
        ]
        labels = {
            "is_absent": "欠勤",
            "notes": "備考",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.target_date = kwargs.pop("target_date", date.today())
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        is_absent = cleaned_data.get("is_absent")
        physical = cleaned_data.get("physical")
        mental = cleaned_data.get("mental")

        # 欠勤時：スコアは NULL
        if is_absent:
            cleaned_data["physical"] = None
            cleaned_data["mental"] = None
        else:
            if physical is None or mental is None:
                raise forms.ValidationError(
                    "欠勤でない場合は、肉体・精神スコアの両方が必須です。"
                )

        # 1日1レコード制御
        if Condition.objects.filter(
            user=self.user,
            date=self.target_date
        ).exists():
            raise forms.ValidationError(
                "本日はすでに体調入力が完了しています。"
            )

        return cleaned_data
