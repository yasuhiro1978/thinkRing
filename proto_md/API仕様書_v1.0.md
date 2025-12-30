# API仕様書（API Specification）
## プロジェクト名：Thinking Process App（仮）
## バージョン：v1.0
## 作成者：yasuhiro

---

# 1. 基本仕様

- 形式：REST API
- データ形式：JSON
- 認証：Token または JWT（後で決定）
- ベースURL：`/api/v1/`

---

# 2. エンドポイント一覧

| 機能 | メソッド | エンドポイント |
|------|----------|----------------|
| プロジェクト一覧 | GET | /projects |
| プロジェクト作成 | POST | /projects |
| プロジェクト詳細 | GET | /projects/{id} |
| プロジェクト更新 | PUT | /projects/{id} |
| プロジェクト削除 | DELETE | /projects/{id} |
| 周一覧 | GET | /projects/{id}/rounds |
| 周作成 | POST | /projects/{id}/rounds |
| 周詳細 | GET | /rounds/{id} |
| ステップ一覧 | GET | /rounds/{id}/steps |
| ステップ作成 | POST | /rounds/{id}/steps |
| ノード一覧 | GET | /projects/{id}/nodes |
| ノード作成 | POST | /nodes |
| ノード詳細 | GET | /nodes/{id} |
| ノード更新 | PUT | /nodes/{id} |
| ノードリンク作成 | POST | /nodes/{id}/links |
| ノードリンク一覧 | GET | /nodes/{id}/links |

---

# 3. リクエスト / レスポンス仕様

---

## 3.1 プロジェクト

### POST /projects  
**Request**

{
  "title": "角度測定改善",
  "category": "現場改善"
}

**Response**

{
  "id": 1,
  "title": "角度測定改善",
  "status": "active",
  "createdAt": "...",
  "updatedAt": "..."
}

## 3.2 Round(周)

### POST/project/{id}/rounds
**Request**

{
  "roundNumber": 2,
  "note": "なんか思いついた？ → 測定の流れをもっと簡単にしたい"
}

**Response**

{
  "id": 10,
  "projectId": 1,
  "roundNumber": 2,
  "note": "...",
  "createdAt": "..."
}

## 3.3 ProcessStep

### POST/rounds/{id}/steps
**Request**

{
    "stepType":"overview",
    "content":"目的:作業者の負担軽減"d
}

**Response**
{
  "id": 30,
  "roundId": 10,
  "stepType": "overview",
  "content": "...",
  "createdAt": "..."
}

## 3.4 Node

### POST/nodes
**Request**
{
  "projectId": 1,
  "roundId": 10,
  "stepId": 30,
  "title": "測定",
  "context": "角度、誤差、作業者負担"
}

**Response**
{
  "id": 100,
  "title": "測定",
  "context": "角度、誤差、作業者負担",
  "roundId": 10,
  "stepId": 30
}

## 3.5 NodeLink
**Request**
{
  "toNodeId": 101,
  "weight": 0.5
}

**Response**
{
  "id": 200,
  "fromNodeId": 100,
  "toNodeId": 101,
  "weight": 0.5
}

## 4 エラーレスポンス

{
  "error": "Not Found",
  "message": "Project not found"
}

