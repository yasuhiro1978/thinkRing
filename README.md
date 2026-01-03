# thinkRing

攻殻機動隊・草薙素子のゴーストを説明するために、  
初心者が一生懸命 AI と一緒に作った、  
**循環・派生型 外部思想装置。**

思考を保存するのではなく、**思考が循環し、変質していく構造そのもの**を扱います。
判断は人が行い、**そこに至る思考の流れやひらめき**を可視化します。


思考プロセスを可視化・管理するためのWebアプリケーションです。プロジェクト、ラウンド、ステップ、ノードの階層構造で思考を整理し、Obsidianプラグインとの連携も可能です。

## 概要

thinkRingは、複雑な思考プロセスを構造化して管理するためのツールです。以下の特徴があります：

- **階層的な思考管理**: プロジェクト → ラウンド → ステップ → ノードの4階層構造
- **RESTful API**: Django REST Frameworkによる堅牢なAPI
- **モダンなフロントエンド**: Svelteによる高速でレスポンシブなUI
- **Obsidian連携**: Obsidianプラグインによる統合
- **Docker環境**: 開発環境の簡単なセットアップ

## 技術スタック

### バックエンド
- **Django 4.2.7**: Python Webフレームワーク
- **Django REST Framework 3.14.0**: RESTful API構築
- **PostgreSQL**: リレーショナルデータベース
- **JWT認証**: セキュアな認証システム

### フロントエンド
- **Svelte 4.2.7**: 軽量で高速なUIフレームワーク
- **Vite 5.0**: モダンなビルドツール

### インフラ
- **Docker & Docker Compose**: コンテナ化された開発環境
- **PostgreSQL 15**: データベースコンテナ

## プロジェクト構成

```
thinkRing/
├── app/
│   ├── backend/          # Django バックエンド
│   │   ├── apps/
│   │   │   ├── core/     # コア機能
│   │   │   ├── projects/ # プロジェクト管理
│   │   │   └── auth/     # 認証
│   │   ├── thinkring/    # Django設定
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── frontend/         # Svelte フロントエンド
│   │   ├── src/
│   │   ├── package.json
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   └── README.md         # 詳細なセットアップ手順
├── obsidian_plugin/       # Obsidianプラグイン
├── proto_md/              # 設計ドキュメント
└── README.md              # このファイル
```

## クイックスタート

### 前提条件

- Docker と Docker Compose がインストールされていること
- Git がインストールされていること

### セットアップ手順

1. **リポジトリのクローン**

```bash
git clone https://github.com/your-username/thinkRing.git
cd thinkRing
```

2. **環境変数の設定**

```bash
cd app

# バックエンド環境変数ファイルの作成
cp .env.backend.example .env.backend
# .env.backendを編集して、SECRET_KEY、DB_PASSWORDなどを設定

# フロントエンド環境変数ファイルの作成
cp .env.frontend.example .env.frontend
# .env.frontendを編集して、API URLなどを設定
```

3. **Docker環境の起動**

```bash
docker compose up -d --build
```

4. **データベースマイグレーション**

```bash
docker compose exec backend python manage.py migrate
```

5. **テストユーザーの作成（オプション）**

```bash
docker compose exec backend python manage.py create_test_user
```

### アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000/api/v1/
- **Django管理画面**: http://localhost:8000/admin/

## 開発

詳細な開発手順については、[app/README.md](app/README.md)を参照してください。

### APIエンドポイント

- `POST /api/v1/auth/register/` - ユーザー登録
- `POST /api/v1/auth/login/` - ログイン
- `GET /api/v1/projects/` - プロジェクト一覧取得
- `POST /api/v1/projects/` - プロジェクト作成
- `GET /api/v1/projects/{id}/` - プロジェクト詳細取得
- `PUT /api/v1/projects/{id}/` - プロジェクト更新
- `DELETE /api/v1/projects/{id}/` - プロジェクト削除

詳細なAPI仕様については、`proto_md/API仕様書_v1.0.md`を参照してください。

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。詳細については、コントリビューションガイドラインを参照してください。

## 関連ドキュメント

- [要件定義](proto_md/用件定義_v1.0.md)
- [API仕様書](proto_md/API仕様書_v1.0.md)
- [データベース設計書](proto_md/データベース設計書_v1.0.md)
- [開発環境セットアップガイド](proto_md/開発環境セットアップガイド_v1.0.md)

