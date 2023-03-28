FROM python:3.10

RUN apt update

COPY . .

RUN pip install poetry

WORKDIR /

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

