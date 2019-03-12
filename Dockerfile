FROM tensorflow/tensorflow:1.13.1-py3

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    pip install --upgrade pip setuptools gunicorn

WORKDIR /app

COPY frontend/dist frontend

COPY backend .

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-w", "4", "-b", ":5000", "app:app" ]