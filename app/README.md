# thinkRing 開発環境

このディレクトリには、thinkRingアプリケーションの開発環境が含まれています。

## ディレクトリ構成

```
app/
├── backend/          # Django バックエンド
│   ├── apps/         # アプリケーション
│   │   ├── core/     # コア機能
│   │   ├── projects/ # プロジェクト管理
│   │   └── auth/     # 認証
│   ├── thinkring/    # Django設定
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Svelte フロントエンド
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## クイックスタート

### 1. 環境変数の設定

```bash
# 環境変数ファイルを作成（必要に応じて編集）
cat > .env.backend << EOF
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=thinkring_db
DB_USER=thinkring_user
DB_PASSWORD=thinkring_password
DB_HOST=db
DB_PORT=5432
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=7
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF

cat > .env.frontend << EOF
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000
EOF
```

### 2. Docker環境の起動

```bash
# Docker環境のビルドと起動
docker compose up -d --build

# ログの確認
docker compose logs -f
```

### 3. データベースマイグレーション

```bash
# マイグレーションの実行
docker compose exec backend python manage.py migrate

# テストユーザーの作成（オプション）
docker compose exec backend python manage.py create_test_user
```

### 4. 動作確認

- **バックエンド**: http://localhost:8000
- **フロントエンド**: http://localhost:3000
- **API**: http://localhost:8000/api/v1/

## 完了条件の確認

Phase 1の完了条件：

- [x] `docker-compose up` で環境が起動する
- [x] データベースに接続できる
- [x] ログインAPIが動作する

### ログインAPIのテスト

```bash
# テストユーザーでログイン
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# レスポンス例:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }
```

## 詳細

詳細なセットアップ手順は、`../proto_md/開発環境セットアップガイド_v1.0.md` を参照してください。
