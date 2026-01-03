# thinkRing 開発用 初期プロンプト（Reference Prompt）
## バージョン：v1.0
## 目的
この文書は、Cursor に「thinkRing」アプリの開発を開始させるための  
**プロジェクト概要・MVP仕様・実装方針** をまとめたものです。

thinkRing は、ユーザーの思考プロセスを構造化し、  
文脈付きノードとして保存する Web アプリケーションです。

---

# 1. プロジェクト概要

## 1.1 アプリ名
**thinkRing**

## 1.2 コンセプト
- 思考を 1〜5 周のループとして構造化する  
- 各ステップで生まれたキーワードを「ノード（カード＋文脈）」として保存  
- 思考のつながりを可視化する（MVPでは簡易版）

## 1.3 MVPの目的
- 最小限の機能で「thinkRing の本質」を動かす  
- まずは **1周目の思考プロセス** と **ノード登録** ができれば成立する

---

# 2. MVPに含める機能（In Scope）

## 2.1 プロジェクト管理
- プロジェクト作成  
- プロジェクト一覧  
- プロジェクトを開く  

## 2.2 思考プロセス（1周目のみ）
5ステップを入力・保存できること：

1. 俯瞰  
2. 要素抽出  
3. 流れ構築  
4. 最小仕様  
5. 拡張余地  

## 2.3 ノード（カード＋文脈）
- ノードの手動登録  
  - title  
  - context  
  - projectId  
  - stepId  
- ノード一覧  
- ノード詳細  

---

# 3. MVPに含めない機能（Out of Scope）

以下は後で追加するため、MVPでは実装しない：

- 2〜5周の改善ループ  
- ノードリンク（NodeLink）  
- ノードツリー（グラフ表示）  
- プロジェクト状態管理（pending/completed）  
- PWA（オフライン対応）  
- 自動キーワード抽出  
- AI補完  
- チーム共有  
- PDF/Markdown出力  

---

# 4. 技術スタック（Tech Stack）

## Backend
- Python  
- Django  
- Django REST Framework  

## Frontend
- Svelte（推奨）  
- または React  

## Database
- PostgreSQL  

## Infra
- Docker（backend / frontend / db）  

---

# 5. データモデル（MVP版）

## Project
- id  
- title  
- createdAt  
- updatedAt  

## Round（1周目のみ）
- id  
- projectId  
- roundNumber = 1  
- createdAt  

## ProcessStep
- id  
- projectId  
- roundId  
- stepType  
- content  

## Node
- id  
- projectId  
- roundId  
- stepId  
- title  
- context  

---

# 6. API（MVP版）

## Project
- GET /projects  
- POST /projects  
- GET /projects/{id}  

## Round
- POST /projects/{id}/rounds  
- GET /rounds/{id}  

## Step
- POST /rounds/{id}/steps  
- GET /rounds/{id}/steps  

## Node
- POST /nodes  
- GET /projects/{id}/nodes  
- GET /nodes/{id}  

---

# 7. 実装方針（Cursorへの指示）

1. **まず Django プロジェクトを作成する**  
2. **次に Django モデル（Project / Round / ProcessStep / Node）を実装する**  
3. **Django REST Framework で API を作成する**  
4. **Svelte（または React）でフロントの骨格を作る**  
5. **MVPの画面（5画面）を順に実装する**  
6. **Docker で backend / frontend / db を統合する**

---

# 8. 完成条件（Definition of Done）

- プロジェクトを作成できる  
- 1周目の5ステップを入力・保存できる  
- ノードを手動で登録できる  
- ノード一覧と詳細が見られる  
- 最低限のUIで操作できる  

---

# 9. 備考
この文書は MVP 開発のための最小仕様です。  
詳細仕様（要件定義書・画面仕様書・API仕様書）は別途参照してください。