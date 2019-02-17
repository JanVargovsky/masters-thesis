FROM tensorflow/tensorflow:1.12.0-py3

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    pip install --upgrade pip setuptools openpyxl

WORKDIR /app

COPY frontend/dist frontend

COPY backend .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]