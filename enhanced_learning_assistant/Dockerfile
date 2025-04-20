FROM python:3.13-alpine

WORKDIR /app

# Optional: Install build dependencies if needed (e.g., for numpy, pandas)
# apk add --no-cache build-base

# Upgrade pip and install app dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
