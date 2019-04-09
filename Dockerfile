FROM node:lts-alpine as frontend-build
WORKDIR /app
COPY frontend .
RUN yarn install
RUN yarn build

FROM tensorflow/tensorflow:1.13.1-py3
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    pip install --upgrade pip setuptools gunicorn
WORKDIR /app
#COPY frontend/dist frontend
COPY --from=frontend-build /app/dist frontend
COPY backend .
RUN pip install -r requirements.txt
CMD [ "gunicorn", "-w", "4", "-b", ":5000", "--log-level", "debug", "--timeout", "3600", "app:app" ]
