# 7. ご意見箱モジュール詳細設計（Feedback Module）

本章では、PHP で実装される「ご意見箱」機能の詳細仕様を定義する。  
本機能は Django 本体とは独立して動作し、CSV を介して連携する。

---

## 7.1 目的

- 社員が匿名・準匿名・署名のいずれかで自由に意見を投稿できる場を提供する  
- 投稿内容は職場改善や分析の基礎データとして活用できる  
- 匿名性と利便性を両立した UI/UX を実現する  
- Django 側に余計な依存を持たせない（CSV 連携）

---

## 7.2 構成概要

```text
php_opinion_box/
├── index.php        ← 投稿形式選択
├── form.php         ← 入力画面
├── confirm.php      ← 確認画面
├── submit.php       ← CSV保存処理
├── success.php      ← 完了画面
├── css/style.css
├── js/validation.js
└── opinions/opinion_box.csv
```
（追記）

【Django との連携仕様（employee_id）】
- Django 側でログイン後に取得した employee_id を、
  `index.php?id=xxxxx` のように URL パラメータとして受け取る。
- 受け取った employee_id は form.php → confirm.php → submit.php と
  hidden フィールドで引き継ぎ、CSV の employee_id カラムとして保存する。

---

## 7.3 投稿形式選択（index.php）

### ● 7.3.1 選択肢
| 種類   | 内容             | 取得情報               |
| ------ | ---------------- | ---------------------- |
| 匿名   | 完全匿名で投稿   | 取得なし               |
| 準匿名 | 年代・性別       | gender, age_range      |
| 署名   | 個人情報付き投稿 | 氏名・部署・年齢・性別 |

### ● 7.3.2 表示仕様  
- 3つのボタン（匿名／準匿名／署名）を横並びまたは縦並びで表示  
- 押下すると説明モーダル（または説明画面）を表示  
- 「進む」ボタンで `form.php` へ遷移

---

# 7.4 入力画面（form.php）

### ● 入力項目（モードによって変化）

| 項目                    | 匿名 | 準匿名          | 署名            |
| ----------------------- | ---- | --------------- | --------------- |
| 性別                    | -    | Django 側で補完 | Django 側で補完 |
| 年代                    | -    | Django 側で補完 | Django 側で補完 |
| 氏名                    | -    | -               | Django 側で補完 |
| 部署                    | -    | -               | Django 側で補完 |
| 意見本文（content）     | ○    | ○               | ○               |
| タグ（カテゴリ）（tag） | ○    | ○               | ○               |

※ 準匿名・署名モードで必要となる個人情報（性別・年代・部署・氏名）は、  
　employee_id を元に Django 側の DB から補完するため、  
　PHP 側で入力欄を設けない仕様とする。

---

### ● タグ候補（カテゴリ分類）

- 業務改善  
- 人間関係  
- 設備・環境  
- 安全性  
- その他

---

### ● 入力チェック仕様

- 意見本文（content）は必須  
- タグ（tag）は必須  
- mode と employee_id は hidden として保持し、次画面へ POST  
- content のエスケープ処理は confirm.php で実施  
- 個人情報は Django 側が補完するため PHP 側では不要

---

### ● 画面遷移仕様

1. index.php  
   利用者ID（employee_id）と投稿モード（mode）を選択し form.php へ POST  

2. form.php  
   content（意見本文）と tag（カテゴリ）を入力し confirm.php へ POST  
   このとき、以下の値を hidden で保持して引き渡す  
   - employee_id  
   - mode  
   - tag  
   - content（未エスケープ）

3. confirm.php  
   content のエスケープ処理を行い、確認画面として表示する

---

## 7.5 確認画面（confirm.php）

### ● 表示内容

confirm.php では、利用者が送信前に以下の内容を確認できる画面を表示する。

- 意見本文（content）  
- 投稿形式（mode：匿名 / 準匿名 / 署名）  
- タグ（カテゴリ：tag）

※ employee_id は利用者に表示しない。  
　（内部処理用のキーであり公開不要のため）

---

### ● 表示仕様

- content は confirm.php の内部で htmlspecialchars によりエスケープし、  
  XSS 誘発文字を安全な表示形式へ変換してから表示する。
- mode は以下の対応表により日本語化したラベルを表示する。

| mode値    | 表示ラベル |
| --------- | ---------- |
| anonymous | 匿名       |
| semi      | 準匿名     |
| signed    | 署名       |

- tag は選択されたカテゴリ名をそのまま表示する。

---

### ● 隠し項目（POSTでの保持）

confirm.php から submit.php に送信する際、  
以下の値を hidden input として保持し POST で渡す。

- employee_id  
- mode  
- content（エスケープ済み値）  
- tag  
- timestamp（submit.php 側で生成するため confirm.php では不要）

---

### ● 画面遷移仕様

- 「戻る」ボタン  
  form.php に戻り、再編集できるようにする。  
  mode / employee_id / content / tag は hidden で保持し、編集が可能。

- 「送信」ボタン  
  submit.php に POST され、CSV 書き込み処理へ進む。

---

### ● 確認画面の目的

- 利用者に入力内容の最終確認を促す  
- 不要な編集ミス・タグ選択ミスを防ぐ  
- エスケープ済みの実際に保存される値を確認できる状態にする

---

## 7.6 投稿処理（submit.php）

### ● 処理内容

submit.php は、confirm.php から POST されたデータを受け取り、  
CSV ファイルに 1レコードとして書き込む役割を持つ。

処理の流れは以下の通り。

1. POST データの取得  
2. timestamp の生成（サーバー側で付与）  
3. CSV 行データの整形  
4. CSV への追記（append モード）  
5. success.php へのリダイレクト

---

### ● POST で受け取る値

confirm.php から POST される値は以下の通り。

- employee_id  
- mode  
- content（エスケープ済み）  
- tag  

※ 個人情報（部署・性別・年代・氏名）は Django 側の DB で補完するため、  
　PHP 側の CSV には含めない仕様とする。

---

### ● timestamp の生成仕様

timestamp は PHP の date 関数で生成する。

```php
$timestamp = date('Y-m-d H:i:s');
```

※ すべての投稿に投稿時刻を付与することで、  
　Django 側での分析（時系列分析など）に利用可能とする。

---

### ● CSV 書き込み形式（1レコード）

CSV は 1行1投稿とし、以下の形式で追記する。

```csv
timestamp, employee_id, mode, content, tag
2025-11-25 10:00:00, test001, signed, "意見本文", "業務改善"
```

---

### ● CSV 保存仕様

- 文字コード：UTF-8（BOMなし）  
- 追記モード（a）で開く  
- fputcsv により安全に CSV 形式へ変換して保存  
- CSV は Django 側の分析用モジュールから読み込む前提

CSV の保存先は、php_opinion_box ディレクトリ内の以下とする。

```text
php_opinion_box/
└── opinions/
    └── opinion_box.csv
```

---

### ● ファイルエラー時の扱い

- ファイルが開けなかった場合は CSV に保存せず、  
　エラー用の画面（またはメッセージ）へ遷移させる  
- 本システムでは想定最低限の実装として、  
　書き込みエラーは管理者が手動で確認する運用とする

---

### ● 送信後の遷移

CSV への保存が完了したら、

- header("Location: success.php");  
- exit;  

により success.php へ遷移する。

success.php では、利用者へ投稿完了メッセージを表示し、  
5秒後にログイン画面へ自動遷移する仕様とする。

---

## 7.7 完了画面（success.php）

### ● 表示内容

submit.php による CSV 書き込み処理が正常に完了した場合、  
success.php を表示する。

ユーザーには以下の内容を提示する。

- 「投稿が完了しました」というメッセージ  
- 「ご協力ありがとうございました」などの完了案内  
- 5秒後にログイン画面へ自動遷移する旨の案内文  
- 手動でログイン画面へ戻れるリンク

---

### ● 自動遷移仕様

success.php では  
meta refresh を用いて **5秒後に Django のログイン画面へ戻す**。

```html
<meta http-equiv="refresh" content="5;URL=http://localhost:8000/login/">
```

遷移先 URL は Django 側のログイン画面 URL とする。  
（開発環境に応じて適宜変更可能）

---

### ● 手動戻りリンク

ユーザーが即時戻りたい場合のために、  
success.php 内に以下のリンクを設置する。

```html
<a href="http://localhost:8000/login/">ログイン画面へ戻る</a>
```

---

### ● 画面遷移の目的

- 投稿完了後、同じ index.php へ戻すと employee_id が喪失する問題があるため  
　**必ずログイン画面（Django側）に戻す設計とする**

- ご意見箱は Django のサブ機能であるため、  
　PHP 側でループ的に操作させず、  
　ログイン画面への帰還によってシステム構造の整合性を維持する。

---

### ● 例外扱い

- 投稿完了後に index.php に戻す導線は用意しない  
- success から index に戻したい場合は ID の再受け渡しが必要になるため、  
　本システム設計では採用しない


---

## 7.8 セキュリティ対策

ご意見箱モジュール（PHP）は Django 本体とは独立稼働する構成であるため、  
PHP 側で想定される攻撃に対して最低限必要な対策を実施する。

### ● XSS（クロスサイトスクリプティング）対策

- confirm.php にて、content（意見本文）を  
  htmlspecialchars によりエスケープしてから表示する。  
- content を hidden の値として submit.php へ渡す際も  
  エスケープ済み値を用いることで、表示・保存の双方で XSS を防止する。

```php
$comment = htmlspecialchars($_POST['content'], ENT_QUOTES, 'UTF-8');
```

---

### ● CSV インジェクション対策

Excel が `=`, `+`, `-`, `@` で始まる値を  
「関数」と誤認するケースに備え、  
content および tag の値がこれらの文字で始まる場合は  
先頭にシングルクォート（'）を付与して保存する。

（※ php_opinion_box モジュール内で必要に応じて適用する）

---

### ● CSRF 対策

本モジュールはログイン・セッションを持たず、  
Django 側から employee_id を付与された状態で遷移してくる構造であるため、  
一般的な CSRF トークンによる保護は限定的な運用となる。

対策方針：

- form → confirm → submit の遷移はすべて POST のみ  
- 外部リンクから直接 submit.php にアクセスできないように  
  「hidden 値が揃っていない場合はエラー扱い」にする

```php
if (!isset($_POST['employee_id'], $_POST['mode'], $_POST['content'], $_POST['tag'])) {
    exit('不正なアクセスです');
}
```

---

### ● ディレクトリ・ファイルアクセス対策

- CSV 保存先ディレクトリ（opinions）は Web から直接参照されない位置に置く  
- php_opinion_box ディレクトリ直下に .htaccess を配置し、  
  不要なファイルを外部から参照できない設定とする（Apache運用時）

```text
# .htaccess の例
Options -Indexes
```

---

### ● 入力値のバリデーション

- content（意見本文）は必須チェック  
- tag（カテゴリ）は選択必須  
- 空値や null 値が渡された場合はエラーとして form.php へ戻す  
- employee_id と mode は hidden で保持し、欠損時は不正アクセス扱いにする

---

### ● 目的

- PHP 単体で動作するご意見箱モジュールの安全性を確保する  
- Django 側へ渡す CSV の信頼性を維持する  
- 投稿データの改ざん・不正送信を防止する

---

## 7.9 例外処理

ご意見箱モジュールは Django 本体とは独立した PHP 構成であり、  
POST データを連続して引き回す形で動作するため、  
値の欠損や異常入力に備えた例外処理を実装する。

### ● 必須項目の未入力

以下の項目は必須とする。  
どれか 1 つでも欠けている場合はエラー扱いとし、form.php に戻す。

- content（意見本文）  
- tag（カテゴリ）

入力確認（confirm.php）に遷移する前にチェックを行う。

---

### ● hidden 値の欠損（employee_id / mode）

POST の連続処理において以下の値が欠けた場合は、  
外部からの直接アクセスまたは操作ミスと判断し、処理を中断する。

- employee_id  
- mode

これらが存在しない場合はエラー画面を表示し、  
submit.php での CSV 書き込みは行わない。

---

### ● CSV 書き込み失敗時の例外

CSV への保存処理（fputcsv）が失敗した場合は、  
意見が保存されていない可能性があるため  
ユーザーにエラーを通知する。

通知内容の例：

- 「データの保存に失敗しました」  
- 「お手数ですが再度入力をお願いします」

保存失敗時は success.php には遷移しない。

---

### ● 不正アクセス（submit.php の直接アクセス）

submit.php に直接アクセスされた場合や  
必要な値が POST されていない場合は、  
「不正なアクセスです」と表示し処理を終了する。

※ 実装は後回しとし、設計書上の仕様として記載する。

---

### ● 想定外の値（無効値）

mode に関しては以下の 3 種類以外の値は無効とする。

- anonymous  
- semi  
- signed

想定外の値が渡された場合は処理を中止する。

---

### ● 目的

- PHP 側で最低限の入力不整合を検出し、CSV の信頼性を維持する  
- 連続した POST 処理の中で不正・欠損データを排除する  
- Django 側でのデータ分析の前にデータ品質を担保する

---

## 7.10 Django 側との連携仕様（読み込み処理）

ご意見箱モジュール（PHP）は Django 本体とは独立して動作し、  
CSV を介してデータを受け渡す。  
本節では Django 側が CSV を読み込み、  
分析用データとして再構築する仕様を定義する。

---

### ● CSV の構造（PHP 側で出力される形式）

```csv
timestamp, employee_id, mode, content, tag
2025-11-25 12:00:00, test001, signed, "改善してほしい点があります", 業務改善
```

※ 個人情報（氏名・部署・性別・年代）は CSV に含めない。  
※ Django 側で employee_id をキーにして DB から補完する。

---

### ● Django 側で行う処理の流れ

1. PHP 側で出力された CSV を pandas で読み込む  
2. timestamp を datetime 型に変換  
3. employee_id をキーに Django DB の社員マスタから情報を補完  
4. mode に応じて使用する列を調整  
5. 分析用 DataFrame として整形する  
6. グラフ作成・傾向分析に用いる

---

### ● pandas によるデータ読み込み例

```python
import pandas as pd

df = pd.read_csv("php_opinion_box/opinions/opinion_box.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
```

---

### ● Django 側で行う情報補完

employee_id を利用して Django の DB（社員情報テーブル）を参照し、  
mode に応じて必要な情報だけを補完する。

#### ■ 匿名（anonymous）
- 追加で取得する情報：なし  
- すべて "-" として扱う

#### ■ 準匿名（semi）
- 性別（gender）
- 年代（age_range）
※ 氏名・部署は利用しない

#### ■ 署名（signed）
- 氏名（name）
- 部署（department）
- 年齢（age）
- 性別（gender）

---

### ● 補完後の分析 DataFrame（例）

```python
分析用_df = pd.DataFrame({
    "timestamp": df["timestamp"],
    "employee_id": df["employee_id"],
    "mode": df["mode"],
    "content": df["content"],
    "tag": df["tag"],
    "gender": 補完後データ["gender"],
    "age_range": 補完後データ["age_range"],
    "department": 補完後データ["department"],
})
```

mode の値に応じて不要カラムは "-" に置き換える。

---

### ● 分析結果の利用例

- タグ別投稿件数（業務改善・人間関係など）  
- 署名（signed）投稿から部署別傾向の分析  
- 準匿名（semi）投稿から性別・年代の傾向分析  
- 時間帯別の投稿傾向  
- 月別の投稿動向

---

### ● 目的

- PHP 側では最低限のデータのみを保存し、個人情報は Django 側で一元管理する  
- CSV → pandas → Django DB 補完 の流れで正確な分析基盤を構築する  
- モードによる情報制御を Django 側で厳密に運用することで、匿名性・準匿名性を保つ
