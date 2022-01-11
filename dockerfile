FROM python:3.10

ENV SECRET_KEY=hejie

WORKDIR /FastAPI-admin

COPY ./requirements.txt /FastAPI-admin/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /FastAPI-admin/requirements.txt

COPY ./app /FastAPI-admin/app

RUN mkdir /FastAPI-admin/log

VOLUME ["/FastAPI-admin/app/core", "/FastAPI-admin/log"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]