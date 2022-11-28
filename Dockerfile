FROM python:3.11

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home app
WORKDIR /home/app
USER app

COPY --chown=app:app . .

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "./src/main.py"]
