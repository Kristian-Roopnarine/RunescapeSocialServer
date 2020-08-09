FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

WORKDIR /app

COPY ./ /app

RUN pip install -r app/requirements.txt
EXPOSE 5000
COPY ./ /app

CMD ["flask","run","--host","0.0.0.0"]