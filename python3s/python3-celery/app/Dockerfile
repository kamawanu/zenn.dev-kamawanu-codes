# app/Dockerfile
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# デフォルトのコマンドは指定しない（docker-compose.ymlで指定）
