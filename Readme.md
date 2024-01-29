### API GATEWAY SETUP

1. Start FastAPI server on development

`uvicorn main:app --reload --host 0.0.0.0 --port 8000`

2. Start FastAPI server on production

```markdown
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

Adjust the number of workers (-w) according to your server's capacity.

3. Dockerize FastAPI 

```markdown
FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

docker build -t fastapi_gateway .
docker run -p 8000:8000 fastapi_gateway
```
