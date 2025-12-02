# 体調・気分記録テーブル設計（condition_records）

## 1. 概要
社員の日次体調・気分を記録するテーブル。  
- 肉体的・精神的スコアを別々に管理  
- 欠勤や備考情報も保存  
- 将来的な統計・分析や通知機能に対応

---

## 2. カラム設計

| カラム名        | 型       | 制約                                             | 備考                                  |
|-----------------|----------|------------------------------------------------|---------------------------------------|
| record_id       | INT      | PRIMARY KEY, AUTO_INCREMENT                    | レコードID、自動採番                  |
| employee_id     | INT      | NOT NULL, FOREIGN KEY (employees.employee_id) | 社員ID、employees テーブル参照        |
| date            | DATE     | NOT NULL                                       | 記録日                                |
| physical_score  | TINYINT  | NOT NULL, CHECK (physical_score BETWEEN 1 AND 5) | 体調スコア（1〜5）                   |
| mental_score    | TINYINT  | NOT NULL, CHECK (mental_score BETWEEN 1 AND 5) | 気分スコア（1〜5）                   |
| is_absent       | BOOLEAN  | NOT NULL                                      | 欠勤・休暇フラグ                       |
| remarks         | TEXT     | NULL許容                                      | 備考、自由入力（拡張性優先）          |
| created_at      | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP            | 登録日時                              |
| updated_at      | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新日時 |

---

## 3. インデックス設計

| インデックス名       | カラム名      | 用途・理由 |
|----------------------|---------------|------------|
| PK_record            | record_id     | 主キー検索用（自動付与） |
| IDX_employee_date    | employee_id, date | 社員ごとの日次検索、集計用 |
| IDX_physical_score   | physical_score | 体調スコア集計・傾向分析用 |
| IDX_mental_score     | mental_score  | 気分スコア集計・傾向分析用 |
| IDX_is_absent        | is_absent     | 欠勤集計・分析用 |

---

## 4. 補足
- `employee_id` と `date` の組み合わせでユニーク制約を設けると、**1日1回の入力制限**が強制可能  
- `physical_score` と `mental_score` は固定5段階評価  
- `remarks` は将来的な自由入力やコメント機能に対応  
- インデックスは集計・検索頻度が高いカラムに設定し、パフォーマンス向上を意識
