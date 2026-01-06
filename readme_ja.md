# LLM-RAGを用いたナレッジベース質問応答システム

> **[English README here](readme.md)**

FlaskベースのLLMを用いたドキュメントベースQ&A向けの本番環境対応RAGシステム

**バージョン:** 2.0.0 | **更新日:** 2026年1月6日 | **ステータス:** 本番環境対応

## 概要

ドキュメント管理、ベクトル検索(Milvus)、マルチLLMサポート(OpenAI、Qwen)、ストリーミング応答、会話履歴管理を備えた完全なRAGベースのナレッジベースシステム

## 主な機能

- **RAGパイプライン**: ベクトル類似度検索(Milvus) + LLM補完による完全な検索拡張生成
- **マルチフォーマット対応**: PDF、DOCX、TXT、CSV、XLSX、MD、JSONの自動テキスト抽出
- **ベクトル埋め込み**: OpenAI text-embedding-3-small (1536次元) IVF_FLATインデックス
- **複数LLM対応**: OpenAI gpt-4o-mini & Alibaba Qwen qwen-max
- **ストリーミング応答**: Server-Sent Eventsによるリアルタイムの LLM出力
- **会話管理**: JSON保存による完全なCRUDと永続化された履歴
- **非同期処理**: Celery + Redisによるバックグラウンドドキュメントベクトル化
- **インタラクティブUI**: Alpine.js + Tailwind CSSのチャットインターフェース with マークダウンレンダリング
- **マルチKBクエリ**: 複数のナレッジベースを同時にクエリ
- **手動オーバーライド**: セグメント編集と再埋め込みのオンデマンドトリガー

## アーキテクチャ

```text
project/
├── app.py, config.py, helper.py
├── apps/
│   ├── auth/          # セッションベース認証
│   ├── chat/          # RAG Q&A + 会話管理
│   ├── dataset/       # ナレッジベースCRUD + ドキュメント/セグメント管理
│   └── templates/     # Jinja2テンプレート (chat, dataset, auth)
├── extensions/        # Celery, SQLAlchemy, Milvus, Redis, マイグレーション
├── tasks/             # バックグラウンドジョブ (ドキュメント分割、埋め込み)
├── static/            # CSS (Tailwind), JS (Alpine.js)
└── storage/           # アップロードファイル + ログ
```

## システムワークフロー

### ドキュメント処理フロー

```text
ユーザーアップロード → ファイル保存 → Celeryタスクキュー
                                    ↓
                            テキスト抽出 (PDF/DOCX/TXT/CSV/XLSX)
                                    ↓
                            ドキュメントセグメント化 (500文字、100文字オーバーラップ)
                                    ↓
                            セグメント保存 (PostgreSQL)
                                    ↓
                            埋め込み生成 (OpenAI text-embedding-3-small)
                                    ↓
                            ベクトル保存 (Milvus 1536次元ベクトル)
                                    ↓
                            ステータス更新 (完了)
```

### RAG質問応答フロー

```text
ユーザー質問 → 会話コンテキスト (直近3メッセージ)
                        ↓
                埋め込み生成 (OpenAI)
                        ↓
                ベクトル類似度検索 (Milvus TOP_K=3)
                        ↓
                選択されたデータセットでフィルタ
                        ↓
                セグメントコンテンツ取得 (PostgreSQL)
                        ↓
                取得したコンテキストでプロンプト拡張
                        ↓
                LLM生成 (gpt-4o-mini / qwen-max)
                        ↓
                ユーザーへストリーミング応答
                        ↓
                会話履歴に保存
```

## 技術スタック

**バックエンド**: Flask 3.x | PostgreSQL (SQLAlchemy) | Milvus 2.4.4 | Redis | Celery | Gunicorn
**フロントエンド**: Jinja2 | Tailwind CSS | Alpine.js | Marked.js | Font Awesome
**ドキュメント処理**: PyMuPDF | python-docx | pandas | BeautifulSoup4
**AI/ML**: OpenAI API (text-embedding-3-small, gpt-4o-mini) | Qwen API (qwen-max)

## クイックスタート

**前提条件**: Python 3.8+、PostgreSQL、Redis、Milvus 2.4+、OpenAI/Qwen APIキー

```bash
# 1. インストール & セットアップ
pip install -r requirements.txt
createdb llm_rag
flask db upgrade
flask dataset_init_milvus

# 2. 設定 (config.pyを編集 + .envを作成)
echo "OPENAI_API_KEY=your_key" > .env
echo "QWEN_API_KEY=your_key" >> .env

# 3. サービス起動 (2つのターミナル)
python app.py                                                   # ターミナル1
celery -A app.celery worker --loglevel=info --queues=dataset   # ターミナル2

# 4. アクセス
# チャット: http://localhost:5000/chat
# データセット: http://localhost:5000/dataset
# ログイン: admin@qq.com / 123456
```

### 主要設定 (`config.py` + `.env`)

- **データベース**: PostgreSQL接続 (DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
- **Milvus**: ベクトルDB接続 (MILVUS_HOST, MILVUS_PORT)
- **Redis**: Celeryブローカー (CELERY_BROKER_URL, CELERY_RESULT_BACKEND)
- **APIキー**: OPENAI_API_KEY, QWEN_API_KEY (`.env`内)
- **RAG設定**: SEGMENT_LENGTH=500, OVERLAP=100, TOP_K=3
- **アップロード**: MAX_CONTENT_LENGTH=16MB, ALLOWED_EXTENSIONS={txt,pdf,docx,csv,xlsx,md,json}

## データベーススキーマ

**PostgreSQLテーブル**:

- **Dataset**: ナレッジベース (id, name, desc, タイムスタンプ)
- **Document**: アップロードファイル (id, dataset_id, file_name, file_path, status, タイムスタンプ)
- **Segment**: テキストチャンク (id, dataset_id, document_id, order, content, status, タイムスタンプ)
- **Conversation**: チャット履歴 (id, uid, name, messages[JSON], タイムスタンプ)

**Milvusコレクション** (`dataset_collection`):

- スキーマ: id, dataset_id, document_id, segment_id, text_vector[1536次元 FLOAT]
- インデックス: L2距離を用いたIVF_FLAT
- 操作: 式フィルタリングによるsearch, insert, delete, query

## Celeryタスク & CLIコマンド

**バックグラウンドタスク** (キュー: `dataset`):

1. **document_split_task**: アップロード → テキスト抽出 → セグメント化 (500文字、100オーバーラップ) → DB挿入
2. **segment_embed_task**: 埋め込み生成 → Milvusへ保存 → ステータス更新

**Flaskコマンド**:

```bash
flask db migrate/upgrade/downgrade  # DBマイグレーション
flask dataset_init_milvus           # Milvusコレクション初期化
flask dataset_retry_task            # 失敗したタスクの再試行
flask test_milvus                   # Milvus接続テスト
tail -f storage/logs/celery_worker.log  # Celeryログ監視
```

## 使用方法

**ナレッジベース**: データセット作成 → ドキュメントアップロード (自動処理) → セグメント表示/編集

**チャットインターフェース** (`/chat`):

1. LLMモデル (gpt-4o-mini / qwen-max) & ナレッジベースを選択
2. 質問を入力 → ストリーミングRAG応答を取得
3. 会話を管理 (作成、名前変更、削除、切り替え)
4. KB選択時、RAGがTOP_K=3の関連セグメントを取得

**機能**: マークダウンレンダリング、会話コンテキスト、リクエストキャンセル、自動保存

## APIエンドポイント

- **`/auth`**: login, register, logout
- **`/dataset`**: Dataset/Document/Segment CRUD操作
- **`/chat`**: チャットUI、RAG補完 (ストリーミング)、会話CRUD、メッセージ永続化

## 主要実装詳細

**ブループリント**: auth, chat, datasetモジュール with 個別ルーティング

**RAGパイプライン** ([apps/chat/services.py](apps/chat/services.py)):
`retrieve_related_texts()` → 直近3メッセージを埋め込み → Milvus検索 (TOP_K=3) → dataset_idsでフィルタ → セグメントをシステムメッセージとして注入

**ヘルパー関数** ([helper.py](helper.py)):
`get_llm_embedding()`, `get_llm_chat()`, `segment_text()`, `json_response()`

**ステータスフィルタ**: init → indexing → completed / error (色分けバッジ)

## トラブルシューティング

| 問題 | 解決方法 |
|------|----------|
| **ドキュメントが "init"/"indexing" で停止** | Celeryワーカー起動: `celery -A app.celery worker --loglevel=info --queues=dataset` |
| **OpenAI APIエラー** | `.env`に有効な`OPENAI_API_KEY`があるか確認、APIキーの有効期限確認 |
| **DB接続失敗** | PostgreSQL起動確認: `sudo systemctl status postgresql`、`config.py`の認証情報確認 |
| **アップロード失敗** | `storage/files/`の権限確認、ファイル拡張子が許可されているか確認、ディスク容量確認 |
| **Milvusエラー** | 接続テスト: `flask test_milvus`、再初期化: `flask dataset_init_milvus` |
| **Celery起動しない** | Redis確認: `redis-cli ping` は "PONG" を返すはず |
| **"No module named 'fitz'"** | インストール: `pip install PyMuPDF` |

## 本番環境強化

本番環境デプロイ用のオプション機能:

- ユーザー認証 & 認可
- APIレート制限 & JWTトークン
- 監視、ログ、バックアップ/リカバリ
- ロードバランシング & キャッシング
- 回答のソース帰属
- ハイブリッド検索 (ベクトル + キーワード)
- マルチテナントサポート

## ライセンス & コントリビューション

MITライセンス | プルリクエスト歓迎

**使用技術**: Flask | PostgreSQL | Milvus | Redis | Celery | OpenAI
