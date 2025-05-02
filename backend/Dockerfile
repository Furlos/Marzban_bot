# Этап сборки
FROM python:3.12-alpine AS builder

WORKDIR /app

# Установка системных зависимостей
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev

# Установка uv
RUN pip install --no-cache-dir uv

# Создание виртуального окружения
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем сначала только pyproject.toml
COPY pyproject.toml .

# Создаем минимальную структуру проекта
RUN mkdir -p src && \
    touch src/__init__.py && \
    echo "from fastapi import FastAPI\n app = FastAPI()" > src/main.py

# Установка зависимостей
RUN uv pip install --no-cache-dir -e .

# Теперь копируем реальный код
COPY src/ src/

# Финальная установка
RUN uv pip install --no-cache-dir -e . uvicorn

# Финальный этап
FROM python:3.12-alpine

WORKDIR /backend

# Копируем venv из builder
COPY --from=builder /opt/venv /opt/venv

# Копируем только нужные файлы
COPY --from=builder /app/src /backend/src
COPY --from=builder /app/pyproject.toml .

# Настройка окружения
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]