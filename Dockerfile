FROM python:3.10-slim

# locale
ENV TZ=Asia/Tokyo

# app
RUN pip install -U pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD uvicorn --host 0.0.0.0 --port ${PORT} main:app
