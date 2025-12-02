# 社員情報テーブル設計（employees）

## 1. 概要
社員の基本情報を管理するテーブル。  
将来的な統計・検索・拡張性を考慮して設計。

---

## 2. カラム設計

| カラム名          | 型            | 制約                          | 説明                 |
| ------------- | ------------ | --------------------------- | ------------------ |
| employee_id   | INT          | PRIMARY KEY, AUTO_INCREMENT | 社員ID（自動採番）         |
| name          | VARCHAR(50)  | NOT NULL                    | 社員名                |
| age           | INT          | NOT NULL                    | 年齢                 |
| gender        | CHAR(1)      | NULL許容                      | 性別（M/F）            |
| department    | VARCHAR(50)  |                             | 部署名                |
| position      | VARCHAR(5)   |                             | 役職                 |
| card_uid      | VARCHAR(20)  | UNIQUE                      | ICカードUID           |
| password_hash | VARCHAR(255) | NULL許容                      | パスワード（将来利用、ハッシュ保存） |
| created_at    | DATETIME     | NOT NULL                    | 登録日時               |
| updated_at    | DATETIME     | NOT NULL                    | 更新日時               |


---

## 3. インデックス設計

| インデックス名 | カラム名      | 用途・理由 |
|----------------|---------------|------------|
| PK_employee    | employee_id   | 主キー検索用（自動付与） |
| UNQ_card_uid   | card_uid      | ICカード認証用、ユニーク制約 |
| IDX_department | department    | 部署別検索・統計用 |
| IDX_name       | name          | 名前検索・個別参照用 |
| IDX_age        | age           | 年齢別統計・傾向分析用 |

---

## 4. 補足
- `age` にインデックスを追加することで年齢別集計の検索効率を向上  
- `department` と `position` は文字数に余裕を持たせ、将来的な部署名変更や役職拡張にも対応  
- パスワードは現状 NULL 許容だが、将来設定可能な設計  
- インデックスは検索頻度の高いカラムに絞って追加しており、書き込み性能への影響も最小化
