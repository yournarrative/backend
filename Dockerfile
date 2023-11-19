FROM python:3.11-slim

# Create and set the working directory
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./main.py"]
