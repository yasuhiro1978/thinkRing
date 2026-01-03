# thinkRing MVP仕様書（Minimum Viable Product Specification）
## バージョン：v1.1（Global Node 対応）
## 作成者：yasuhiro

---

# 1. 概要（Overview）

thinkRing の MVP（最小実装）は、  
「思考を1周だけ構造化し、文脈付きノードとして保存する」  
というアプリの本質部分に限定する。

v1.1 では、以下を追加する：

- **プロジェクトに紐づかない “グローバルノード” を扱えるようにする**

これにより、  
「スパイラル思考」などの概念的ノードや、  
プロジェクト外の思いつきを保存できる。

---

# 2. MVPに含める機能（In Scope）

## 2.1 プロジェクト管理
- プロジェクト作成  
- プロジェクト一覧  
- プロジェクトを開く  

---

## 2.2 思考プロセス（1周目のみ）
5ステップを入力・保存できること：

1. 俯瞰  
2. 要素抽出  
3. 流れ構築  
4. 最小仕様  
5. 拡張余地  

---

## 2.3 ノード（カード＋文脈）

### 2.3.1 プロジェクトノード
- title  
- context  
- projectId  
- stepId（任意）  
- roundId（任意）

### 2.3.2 グローバルノード（今回追加）
- title  
- context  
- projectId = null  
- stepId = null  
- roundId = null  

### 2.3.3 ノード一覧
- プロジェクトノード一覧  
- グローバルノード一覧（新規）

### 2.3.4 ノード詳細
- title  
- context  
- 紐づき（projectId or “Global”）

---

# 3. MVPに含めない機能（Out of Scope）

- 2〜5周の改善ループ  
- ノードリンク（NodeLink）  
- ノードツリー（グラフ表示）  
- プロジェクト状態管理  
- PWA（オフライン対応）  
- 自動キーワード抽出  
- AI補完  
- チーム共有  
- PDF/Markdown出力  

---

# 4. 画面（Screens）

MVPで必要な画面は6つ（1つ増えた）。

1. ホーム（プロジェクト一覧）  
2. プロジェクト作成  
3. 思考プロセス（1周目）  
4. ノード一覧（プロジェクト）  
5. ノード詳細  
6. **グローバルノード一覧（新規）**  
   - グローバルノード作成  
   - グローバルノード詳細  

---

# 5. API（MVP版）

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
  - projectId: nullable  
- GET /projects/{id}/nodes  
- GET /nodes/global（新規）  
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

## Node（Global Node 対応）
- id  
- projectId（nullable）  
- roundId（nullable）  
- stepId（nullable）  
- title  
- context  
- createdAt  

---

# 7. 技術スタック（Tech Stack）

- Backend：Python / Django / Django REST Framework  
- Frontend：Svelte（または React）  
- DB：PostgreSQL  
- Infra：Docker  

---

# 8. MVPの完成条件（Definition of Done）

- プロジェクトを作成できる  
- 1周目の5ステップを入力・保存できる  
- プロジェクトノードを登録できる  
- **グローバルノードを登録できる（今回追加）**  
- ノード一覧と詳細が見られる  
- 最低限のUIで操作できる  

---

# 9. 今後の拡張（Future Scope）

- 2〜5周の改善ループ  
- ノードリンク  
- ノードツリー（グラフ表示）  
- PWA（オフライン対応）  
- 自動キーワード抽出  
- AI補完  
- プロジェクト状態管理  
- チーム共有