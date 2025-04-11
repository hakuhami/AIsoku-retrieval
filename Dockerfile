# Dockerfile

FROM python:3.12.2

# 作業ディレクトリを作成
WORKDIR /app

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Cloud Run はポート8080をリッスンするため、環境変数PORTを設定（任意）
ENV PORT=8080

# コンテナ起動時に main.py を実行する
CMD ["python", "main.py"]
