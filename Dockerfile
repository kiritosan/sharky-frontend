FROM python:3.11

COPY requirements.txt /tmp

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r /tmp/requirements.txt

# RUN useradd --create-home app
WORKDIR /app
# USER app

# COPY --chown=app:app . .
COPY . .

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "./src/main.py"]

ENV URL=<你的后端地址>