FROM python:3.11-slim
LABEL author="willem"
LABEL email="1121567132@qq.com"
LABEL version="1.0"
LABEL description="backend for Sharky System"

COPY requirements.txt /tmp

RUN pip install -i --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app
COPY . .

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "./src/main.py"]

ENV URL=<你的后端地址>