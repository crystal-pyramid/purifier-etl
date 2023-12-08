FROM python:3.8-slim

WORKDIR /app

# 必要なパッケージのインストール
# gccやその他ビルドツールは、一部のPythonパッケージをインストールする際に必要
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
 && rm -rf /var/lib/apt/lists/*

# Apache Beam[interactive]をインストール
# [interactive]はローカルでのインタラクティブな開発に便利な拡張機能を含む
RUN pip install apache-beam[interactive]
RUN pip install python-binance
RUN pip install dotenv

COPY . /app

EXPOSE 8080

CMD ["python","pipeline.py"]