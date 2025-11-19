# 社員体調管理・ご意見箱システム

本システムは、以下の2つの機能を統合した Web アプリケーションです。

1. **社員体調管理システム（Django）**  
   - 社員が毎日、体調（肉体）・気分（精神）を入力  
   - 管理者は統計を閲覧し、傾向を把握  
   - CSV＋DBを用いたデータ蓄積と pandas による簡易分析  

2. **ご意見箱システム（PHP）**  
   - 匿名／準匿名／署名の3形態で意見を投稿  
   - 投稿内容は CSV として保存  
   - Django から読み取り、分析可能

これらを **共通の Web インターフェース上からアクセス可能** とする構成です。

---

## 📌 目的

- 社員の心身状態を日々可視化し、早期フォローにつなげる  
- 匿名で意見しやすい環境を整え、職場改善に役立てる  
- 将来的に AI 解析などへ拡張できる「データ基盤」を作る  

---

## 🏗 使用技術

### **Backend**
- Python（Django）
- PHP（ご意見箱）

### **Frontend**
- HTML / CSS  
（レスポンシブ対応：アイコンは画面幅により1〜2段変化）

### **Data**
- SQLite（Django側 DB）
- CSV（ご意見箱投稿／分析用中間データ）

### **Analysis**
- pandas（Django内で使用）

### **Version Control**
- Git / GitHub

---

## 📁 構成（Structure）

```text
project/
├── src/                 ← Django アプリ本体
├── php_opinion_box/     ← ご意見箱（PHP）
└── docs/                ← 設計書（章ごと）
    ├── 01_overview.md
    ├── 02_use_cases.md
    ├── 03_requirements.md
    ├── 04_design_system.md
    ├── 05_db_design.md
    ├── 06_system_flow.md
    ├── 07_feedback_module.md
    ├── 08_analysis_module.md
    ├── 09_security_policy.md
    ├── 10_backup_policy.md
    └── 11_update_history.md
```

---

## 🚀 開発の進め方

1. 設計書を章ごとに整備（今やっている作業）  
2. Django・PHPの開発環境構築  
3. 体調入力／ご意見箱／管理者画面を順次実装  
4. pandas を用いた集計＆簡易分析機能  
5. テスト → UI調整 → 完成  

---

## 📅 今後の拡張

- 出退勤データとの連携（勤怠システム）  
- 自動フォロー通知機能（メール）  
- AI 解析（体調と他データの相関分析）  
- モバイル最適化強化  
- ログイン方式の追加（ICカード → パスワード／MFA など）

---

## 👤 開発者

個人開発プロジェクトとして作成。  
ポートフォリオ・学習用および将来の実用化を視野に入れて構築中。

