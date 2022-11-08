FROM python:3.10

RUN apt update

COPY . .

RUN pip install -r requirements.txt

WORKDIR /

CMD uvicorn main:app --reload