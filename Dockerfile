FROM python:alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /telegram_bot

COPY ./requirements.txt ./

RUN python3 -m venv venv
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt
RUN source venv/bin/activate

COPY ./ ./

RUN chmod -R 777 ./