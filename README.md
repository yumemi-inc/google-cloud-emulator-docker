# Google Cloud Emulator Docker with Initialization Hooks

> [!WARNING]
> このプロジェクトは株式会社ゆめみの公式製品ではありません。

## 概要 (Overview)

このプロジェクトは、公式の `google-cloud-cli` Dockerイメージに、コンテナ起動時に初期化スクリプトを実行する機能を追加したものです。
開発環境のセットアップ（例: Pub/Subトピックの作成、Spannerインスタンスの設定など）を自動化し、容易にすることを目的としています。

この初期化フックの仕組みは [LocalStack](https://github.com/localstack/localstack) の初期化メカニズムに影響を受けています。

## 特徴 (Features)

* **初期化フック**: コンテナ内の `/docker-entrypoint-init.d/ready.d/` ディレクトリに配置されたスクリプトを、エミュレータが起動し準備ができた後に自動的に実行します。
  ```
  /
  └─ docker-entrypoint-init.d
    └─ ready.d    <- エミュレーターの準備が完了した後に実行される
  ```
* **サポートするスクリプト**:
  * シェルスクリプト (`.sh`): `bash` で実行されます。
  * Pythonスクリプト (`.py`): `Python 3.11` で実行されます。
* **Python環境**: 以下の主要なGoogle Cloudクライアントライブラリがインストール済みです。  
  バージョンやそれ以外のインストール済みライブラリについては `requirements.txt` を参照してください。
  * `google-cloud-bigtable`
  * `google-cloud-datastore`
  * `google-cloud-firestore`
  * `google-cloud-pubsub`
  * `google-cloud-spanner`
  

## 使い方 (Usage)

`examples/**` に例を用意しています。

### `compose.yaml` を使用してコンテナを起動する

```yaml
# compose.yaml
services:
  pubsub-emulator:
    image: ghcr.io/yumemi-inc/google-cloud-emulator:latest
    command:
      - --emulator=pubsub
      - --port=8085
      # - --project=my-project # その他のgcloud emulator引数も追加可能
    ports:
      - "8085:8085"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8085"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    volumes:
      # ホストの初期化スクリプトディレクトリをコンテナのready.dにマウント
      - ./init.d/:/docker-entrypoint-init.d/ready.d/
```

1. 上記のような `compose.yaml` ファイルを作成します。
2. ホストマシンに初期化スクリプトを配置するディレクトリ（例: `init.d`）を作成します。
3. `init.d` ディレクトリ内に、実行したい `.sh` または `.py` スクリプトを配置します。
4. `docker compose up` コマンドでコンテナを起動します。
5. エミュレータが起動し、ヘルスチェックが成功した後、`init.d` 内のスクリプトが実行されます。

### 初期化スクリプトの例 (Initialization Script Example)

以下は、Pub/Subエミュレータ起動後にトピックを作成するPythonスクリプトの例です (`init.d/01-create-topic.py`)。

```python
from google.cloud import pubsub_v1

def create_topic(project_id, topic_name):
    """Create a new Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    try:
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"Topic created: {topic.name}")
    except Exception as e:
        print(f"Error creating topic: {e}")

create_topic("test-project", "email-notifications")
create_topic("test-project", "push-notifications")
```

同等の内容をシェルスクリプトで書くことも可能です。

```bash
#!/bin/bash

curl -X PUT http://${PUBSUB_EMULATOR_HOST}/v1/projects/test-project/topics/email-notifications
curl -X PUT http://${PUBSUB_EMULATOR_HOST}/v1/projects/test-project/topics/push-notifications
```

※ `entrypoint.sh` は `gcloud beta emulators <emulator_type> env-init` を実行し、関連する環境変数（例: `PUBSUB_EMULATOR_HOST`, `PUBSUB_PROJECT_ID`）を設定します。スクリプト内ではこれらの環境変数を参照してエミュレータに接続できます。

## 今後の展望 (Future Plans)

現在はエミュレータが完全に準備できた後に実行される `ready.d` フックのみをサポートしていますが、将来的には LocalStack のように、初期化プロセスの異なる段階で実行される他のフックポイント（例: 起動直後、シャットダウン前など）の追加も検討しています。
