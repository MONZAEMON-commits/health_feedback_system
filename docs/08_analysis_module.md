# 8. 連携設計（API / Integration）

本章では、Django 側（体調管理システム）と PHP 側（ご意見箱）の間で  
**ファイル連携（CSV）を中心とした安全でシンプルな結合方法** を定義する。

なお、本システムは API での双方向通信は行わず、  
機能の独立性・保守性・学習負荷の低減を優先する。

---

## 8.1 連携方式の基本方針

### ● A. ”非同期ファイル連携” を採用（採用済み）
- Django ⇔ PHP は直接通信しない  
- PHP は投稿データを CSV に書き込む  
- Django は必要に応じて CSV を読む  
- 同一サーバー内のディレクトリ共有で管理する

### ● 採用理由
- 実装が最も簡単（初心者でも確実に構築できる）
- 保守も容易
- セキュリティ面でも API 連携より安全に管理できる
- Django と PHP を完全に独立モジュールとして扱える

---

## 8.2 ディレクトリ構成（共有部分）

```text
project_root/
├── django_app/
│   ├── manage.py
│   ├── health_app/
│   └── analysis_module/
├── php_opinion_box/
│   ├── opinions/
│   │   └── opinion_box.csv
└── shared_data/
    └── （将来の連携ファイル置き場）
```

---

## 8.3 CSV データ連携（更新後）

本節では PHP 側で保存した CSV を Django 側が読み込み、  
社員情報を補完し分析に利用するための連携仕様を定義する。

PHP 側は個人情報を一切保持せず、  
Django 側で employee_id を用いて必要な情報を補完する設計に変更されたため、  
本節の内容を最新仕様に合わせて更新する。

---

### 8.3.1 書き込み仕様（PHP → CSV）

PHP 側では、submit.php にて投稿データを CSV に追記保存する。

保存されるレコード形式は以下のとおり。

```csv
timestamp, employee_id, mode, content, tag
2025-11-25 12:00:00, test001, signed, "改善点があります", 業務改善
```

#### ● 書き込みルール
- fputcsv による追記保存  
- CSV は 1 投稿 = 1 レコード  
- 個人情報（氏名 / 部署 / 性別 / 年代）は **保存しない**  
- 必須項目：employee_id / mode / content / tag  
- content は htmlspecialchars 済みを保存  
- タグは分類分析のため必須  
- Excel 誤認防止のため以下の文字で始まる場合はエスケープ  
  - =, +, -, @

#### ● サンプル PHP 処理（概念的記述）

```php
$fp = fopen('opinions/opinion_box.csv', 'a');
flock($fp, LOCK_EX);           // 排他
fputcsv($fp, [$timestamp, $employee_id, $mode, $content, $tag]);
flock($fp, LOCK_UN);
fclose($fp);
```

#### ● 保存後の遷移
CSV 保存成功後は **success.php → 5秒後 Django ログイン画面へ遷移**する。

---

### 8.3.2 読み取り仕様（Django → pandas）

Django 側は PHP が保存した CSV を読み込み、  
employee_id をキーとして社員DBの情報を補完し、  
分析用 DataFrame を構築する。

```python
df = pd.read_csv("php_opinion_box/opinions/opinion_box.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
```

---

### 8.3.3 Django 側での情報補完仕様（重要）

employee_id により Django の社員DBを参照し、  
以下の情報を取得する。

- gender（性別）  
- age_range（年代）  
- name（氏名）  
- department（部署）  
- age（年齢）

#### ● mode による補完ルール

| mode      | Django が使用する情報  | 使用しない情報   |
| --------- | ---------------------- | ---------------- |
| anonymous | すべて "-"（完全匿名） | 全情報           |
| semi      | gender, age_range      | 氏名・部署・年齢 |
| signed    | 全情報を利用           | なし             |

#### ● 補完後のデータ例

```python
分析用_df = pd.DataFrame({
    "timestamp": df["timestamp"],
    "employee_id": df["employee_id"],
    "mode": df["mode"],
    "content": df["content"],
    "tag": df["tag"],
    "gender": 補完データ["gender"],
    "age_range": 補完データ["age_range"],
    "department": 補完データ["department"],
})
```

---

### 8.3.4 利用方法（分析側）

補完後の DataFrame は以下の用途で使用される。

- タグ別投稿件数集計  
- 部署別傾向（署名モードのみ）  
- 性別・年代別傾向（準匿名）  
- 時間帯別分析  
- 月次の投稿量推移  
- 体調データ（SQLite）との相関分析（将来拡張）

---

### 8.3.5 本仕様の意義

- PHP 側で個人情報を扱わないため安全性が高い  
- Django が employee_id を用いて正確な社員情報を補完できる  
- CSV と DB を統合した分析が可能  
- Django と PHP の疎結合を維持し、保守性を高める


---

## 8.4 セキュリティ対策（連携部）

### ● ファイル権限
- opinions ディレクトリは書き込み可能だが  
  **Web から直接アクセス不可に設定**（.htaccess or サーバ設定）

### ● CSV インジェクション防止
- =、+、-、@ などで始まる値は自動でエスケープする

### ● Django 側での CSV 信頼性チェック
- 行数異常  
- カラム不足  
- 不正データ行削除  
- timestamp パース失敗時のログ記録

---

## 8.5 将来的な API 実装（拡張）

将来的に必要となった場合のみ、次の API 拡張を想定している。

### ● A. Django が提供する REST API  
- 統計データを JSON で返す  
- PHP 側でグラフ表示に流用できる

### ● B. PHP 側の投稿を Django DB に直接保存  
（現状は非採用）

### ● C. OAuth/Token 認証 API による通信

---

## 8.6 API 利用の分類（現状）

| 項目           | Django | PHP | 現状の扱い          |
| -------------- | ------ | --- | ------------------- |
| 体調記録入力   | ○      | ×   | Django MVC 内で完結 |
| 統計データ取得 | ○      | ×   | Django 内部処理のみ |
| 意見投稿       | ×      | ○   | PHP が単独で処理    |
| 投稿データ参照 | ○      | ×   | CSV 読み取りで対応  |
| API コール     | △      | △   | 拡張のみ            |

---

## 8.7 エラー時の挙動

### ● PHP 側
- CSV 書き込み失敗 → エラー画面  
- 投稿内容不備 → 入力画面へ戻す  
- ディレクトリ権限異常 → 管理者にメール通知（任意）

### ● Django 側
- CSV パースエラー → 該当行をスキップ  
- ファイル未発見 → エラーログに記録  
- 読み込み途中失敗 → 再読込処理（リトライ1回）

---

## 8.8 テスト項目（CSV 連携確認）

| No  | 内容                       | 期待結果             |
| --- | -------------------------- | -------------------- |
| 1   | PHP 側で投稿 → CSV に追記  | 正常に保存される     |
| 2   | Django 側で CSV を読み込み | DataFrame に変換成功 |
| 3   | 不正形式の CSV 行          | スキップされログ記録 |
| 4   | 日本語文字列の保存         | 文字化けしない       |
| 5   | 高負荷時の連続投稿         | CSV が壊れない       |
| 6   | 空行の混入                 | 自動で削除される     |

---

## 8.9 まとめ

本章の内容により、  
Django × PHP の “ゆるく安全な連携” が成立する。

- ファイル連携はシンプルで構築しやすい  
- API を使わないため学習コストが低い  
- しかし将来的に REST API を追加できる柔軟性も保持  
- 体調管理（Django）とご意見箱（PHP）の独立性を保てる

