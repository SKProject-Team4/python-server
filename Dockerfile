FROM python:3.11.9-slim

WORKDIR /app

COPY api/ ./api/
COPY router/ ./router/
COPY src/ ./src/
COPY util/ ./util
COPY requirements.txt ./requirements.txt

RUN mkdir ./save_chat

RUN pip install -r requirements.txt

RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port=1542"]