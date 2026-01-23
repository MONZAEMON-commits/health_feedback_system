# 実装ルール（Implementation Rules）

## 大原則
- 実装は必ず以下の設計書に準拠する
- 設計変更は禁止（補完・最適化・独自判断すべて禁止）
- 不足情報がある場合は  
  「どの設計書・どの章が必要か」を明示して実装を止める

## 参照対象の設計書（FIX）
本プロジェクトでは、以下の設計書を正式仕様とする。

- 01_overview.md  
- 02_use_cases.md  
- 03_requirements.md  
- 04_design_system.md  
- 05_db_design.md  
- 06_system_flow.md  
- 07_feedback_module.md  
- 08_analysis_module.md  
- 09_security_policy.md  
- 10_backup_policy.md  
- 11_update_history.md  

※ 上記以外の文書・口頭説明・推測は仕様として扱わない

---

## 実装の進め方
- 1ステップずつ進める（まとめて実装しない）
- 手順提示は最大3つまで
- 実装前に必ず  
  **参照する設計書（ファイル名 + 章番号）を明示する**
- 迷った場合は実装せず、設計書確認に戻る

---

## テンプレート運用ルール
- Django template に不要なコメントアウトを入れない  
  （テンプレート構文エラーの原因になるため）
- 表示制御は view 側で行い、template は最小限に保つ
- 見た目（CSS・ボタン統一・装飾）は最終フェーズでまとめて行う

---

## バージョン・前提条件
- Django 5 系前提
- ログアウトは POST のみ許可する仕様に準拠
- セキュリティ要件は `09_security_policy.md` を最優先で参照する
