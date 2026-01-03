# トラブルシューティングガイド

## バックエンドが起動しない場合

### 1. コンテナの状態を確認

```bash
cd /Volumes/sd_yasuwo/programming/thinkRing/app

# コンテナの状態を確認
docker compose ps

# すべてのコンテナ（停止中も含む）を確認
docker compose ps -a
```

### 2. バックエンドのログを確認

```bash
# バックエンドのログを確認
docker compose logs backend

# リアルタイムでログを確認
docker compose logs -f backend
```

### 3. よくあるエラーと解決方法

#### エラー: データベース接続エラー

**症状**: `django.db.utils.OperationalError: could not connect to server`

**解決方法**:
```bash
# データベースコンテナが起動しているか確認
docker compose ps db

# データベースのログを確認
docker compose logs db

# データベースコンテナを再起動
docker compose restart db

# バックエンドを再起動
docker compose restart backend
```

#### エラー: マイグレーションが実行されていない

**症状**: `django.db.utils.ProgrammingError: relation "django_migrations" does not exist`

**解決方法**:
```bash
# マイグレーションを実行
docker compose exec backend python manage.py migrate
```

#### エラー: 環境変数が見つからない

**症状**: `KeyError` や環境変数関連のエラー

**解決方法**:
```bash
# .env.backendファイルが存在するか確認
ls -la .env.backend

# ファイルが存在しない場合は作成
# README.mdの手順を参照
```

#### エラー: ポートが既に使用されている

**症状**: `Error: bind: address already in use`

**解決方法**:
```bash
# ポート8000を使用しているプロセスを確認
lsof -i :8000

# プロセスを終了
kill -9 <PID>
```

### 4. 完全にクリーンアップして再起動

```bash
# すべてのコンテナを停止・削除
docker compose down

# ボリュームも削除（データベースのデータも削除される）
docker compose down -v

# 再ビルドして起動
docker compose up -d --build

# ログを確認
docker compose logs -f
```

### 5. バックエンドコンテナに直接入って確認

```bash
# コンテナに入る
docker compose exec backend bash

# コンテナ内で以下を実行
python manage.py check
python manage.py showmigrations
python manage.py migrate
```

### 6. データベース接続の確認

```bash
# データベースコンテナに入る
docker compose exec db psql -U thinkring_user -d thinkring_db

# PostgreSQLシェルで以下を実行
\dt  # テーブル一覧を表示
\q   # 終了
```

## フロントエンドが起動しない場合

### 1. ログを確認

```bash
docker compose logs frontend
```

### 2. 依存関係の再インストール

```bash
# コンテナを再ビルド
docker compose up -d --build frontend
```

## その他の問題

### Docker Composeコマンドが見つからない

```bash
# 新しい形式（推奨）
docker compose up -d

# 古い形式（別途インストールが必要）
docker-compose up -d
```

### 拡張属性ファイルのエラー

```bash
# 拡張属性ファイルを削除
find . -name "._*" -type f -delete
```

