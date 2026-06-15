FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量，防止 python 缓冲 stdout/stderr
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（newspaper3k 需要的一些依赖，如 libxml2 等）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 下载 NLTK 数据 (newspaper3k 依赖)
RUN python -m nltk.downloader punkt

# 复制项目代码
COPY . /app/

# 暴露端口 (云托管通常要求监听 80 端口)
EXPOSE 80

# 启动命令：运行 FastAPI，同时在 main.py 中会启动后台调度器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
