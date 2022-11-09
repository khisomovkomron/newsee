FROM python:3.10

RUN apt update

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /

#CMD uvicorn main:app --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]