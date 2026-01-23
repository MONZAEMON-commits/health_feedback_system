# 現在地（Current Status）

## 完了
- accounts：認証・権限（Django 5 前提）完了
- dashboard：管理者ダッシュボード基盤 + 集計表示 完了
- analysis：CSV 読み込み（CSV未存在/空でも落ちない）完了
- CSV：タグ別件数を dashboard に表示できる状態（フェーズ42完了）

## 方針
- 見た目調整は最後にまとめて実施する

## 次の候補フェーズ（選択待ち）
A. analysis 本格化
- mode（anonymous/semi/signed）による匿名化制御
- CSV × DB 突合（employee_id）

B. 一般ユーザー体調入力画面
- ModelForm
- 当日1件制御
- 欠勤対応
- 完了後ログアウト
