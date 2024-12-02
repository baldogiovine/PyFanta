FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt

COPY src /app/src

WORKDIR /app

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
