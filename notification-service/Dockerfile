FROM python:3.9.5

ENV HOME=/code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN addgroup web && adduser web --home $HOME --ingroup web
RUN mkdir /var/log/gunicorn/ && chown -R web:web /var/log/gunicorn/
RUN mkdir /var/run/gunicorn/ && chown -R web:web /var/run/gunicorn/
RUN mkdir $HOME/static && chown -R web:web $HOME/static

WORKDIR $HOME

COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY src .
COPY ./entrypoint.sh /usr/local/bin

USER web
