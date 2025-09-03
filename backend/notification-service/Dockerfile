FROM python:3.10-slim

WORKDIR /app

COPY ./src /app/src
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]
