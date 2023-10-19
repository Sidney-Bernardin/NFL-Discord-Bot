FROM python:3.9.2 AS test

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "test_data.py"]

# ============================================================================

FROM python:3.9.2

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
