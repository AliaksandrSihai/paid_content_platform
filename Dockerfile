FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR paid_content/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
