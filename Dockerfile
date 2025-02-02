FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

#FastAPI is running on port 8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]