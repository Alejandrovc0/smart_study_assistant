FROM python:3.12.14

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 8000

CMD ["python", "app.py"]