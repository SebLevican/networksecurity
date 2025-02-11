FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt
RUN pip install uvicorn

# Cambiar las comillas simples por dobles y usar array correcto
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
