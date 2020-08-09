FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /work

COPY ./ /work

RUN pip install -r app/requirements.txt
EXPOSE 5000
COPY ./ /work

CMD ["flask","run","--host","0.0.0.0"]