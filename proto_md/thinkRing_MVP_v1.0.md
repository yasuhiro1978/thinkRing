# thinkRing MVP仕様書（Minimum Viable Product Specification）
## バージョン：v1.0
## 作成者：yasuhiro

---

# 1. 概要（Overview）

thinkRing の MVP（最小実装）は、  
「思考を1周だけ構造化し、文脈付きノードとして保存する」  
というアプリの本質部分に限定する。

MVPでは以下の3つが動けば成立する：

1. プロジェクトを作成できる  
2. 1周目の思考プロセス（5ステップ）を入力・保存できる  
3. ノード（カード＋文脈）を手動で登録し、一覧表示できる  

---

# 2. MVPに含める機能（In Scope）

## 2.1 プロジェクト管理（最小）
- プロジェクト作成  
- プロジェクト一覧表示  
- プロジェクトを開く  

※ 状態（pending/completed）はMVPでは不要

---

## 2.2 思考プロセス（1周目のみ）

### 5ステップ
1. 俯瞰  
2. 要素抽出  
3. 流れ構築  
4. 最小仕様  
5. 拡張余地  

### 必須要件
- 各ステップの入力フォーム  
- 入力内容の保存  
- 1周目のまとめ画面  

### 含めないもの
- 2〜5周の改善ループ  
- 「なんか思いついた？」入力  
- 周カウンター  

---

## 2.3 ノード（カード＋文脈）

### MVPで必要な機能
- ノードの手動登録  
  - title（カード名）  
  - context（文脈）  
  - projectId  
  - stepId  

- ノード一覧表示  
- ノード詳細表示  

### 含めないもの
- 自動キーワード抽出  
- ノードリンク（線）  
- ノードツリー（グラフ表示）  

---

# 3. MVPに含めない機能（Out of Scope）

以下はMVPでは実装しない：

- 2〜5周の改善ループ  
- ノードリンク（NodeLink）  
- ノードツリー（グラフ可視化）  
- プロジェクト状態管理（pending/completed）  
- PWA（オフライン対応）  
- 自動キーワード抽出  
- AI補完  
- チーム共有  
- PDF/Markdown出力  

---

# 4. 画面（Screens）

MVPで必要な画面は5つ。

1. **ホーム（プロジェクト一覧）**  
2. **プロジェクト作成**  
3. **思考プロセス（1周目）**  
   - 俯瞰  
   - 要素抽出  
   - 流れ構築  
   - 最小仕様  
   - 拡張余地  
4. **ノード一覧**  
5. **ノード詳細**

---

# 5. API（MVP版）

必要なAPIは以下のみ。

## 5.1 プロジェクト
- GET /projects  
- POST /projects  
- GET /projects/{id}  

## 5.2 Round（1周目のみ）
- POST /projects/{id}/rounds  
- GET /rounds/{id}  

## 5.3 Step（5ステップ）
- POST /rounds/{id}/steps  
- GET /rounds/{id}/steps  

## 5.4 Node（手動登録）
- POST /nodes  
- GET /projects/{id}/nodes  
- GET /nodes/{id}  

---

# 6. データモデル（MVP版）

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

※ NodeLink はMVPでは不要

---

# 7. 技術スタック（MVP版）

- Backend：Python / Django / Django REST Framework  
- Frontend：Svelte（または React）  
- DB：PostgreSQL  
- Infra：Docker（backend / frontend / db）  

---

# 8. MVPの完成条件（Definition of Done）

- プロジェクトを作成できる  
- 1周目の5ステップを入力・保存できる  
- ノードを手動で登録できる  
- ノード一覧と詳細が見られる  
- 最低限のUIで操作できる  

これらが動けば **thinkRing の本質は成立する**。

---

# 9. 今後の拡張（Future Scope）

MVP後に追加する機能：

- 2〜5周の改善ループ  
- ノードリンク  
- ノードツリー（グラフ表示）  
- PWA（オフライン対応）  
- 自動キーワード抽出  
- AI補完  
- プロジェクト状態管理  
- チーム共有