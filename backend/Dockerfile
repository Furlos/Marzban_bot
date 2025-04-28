# Этап сборки
FROM python:3.12-alpine AS builder

WORKDIR /app

# Установка системных зависимостей
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev

# Установка uv
RUN pip install --no-cache-dir uv

# Создание виртуального окружения
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем зависимости
COPY pyproject.toml .

# Установка зависимостей
RUN uv pip install --no-cache-dir . uvicorn

# Финальный этап
FROM python:3.12-alpine

WORKDIR /backend

# Копируем venv из builder
COPY --from=builder /opt/venv /opt/venv

# Копируем исходный код (включая backend директорию)
COPY . .

# Настройка окружения
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend

# Очистка кешей
RUN find /backend -type d -name '__pycache__' -exec rm -rf {} + && \
    find /backend -type f -name '*.pyc' -delete

EXPOSE 3000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]