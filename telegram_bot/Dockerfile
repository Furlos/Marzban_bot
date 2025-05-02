# Этап сборки
FROM python:3.13-slim as builder

WORKDIR /frontend

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Копируем только файлы зависимостей
COPY pyproject.toml uv.lock ./

# Создаем виртуальное окружение и устанавливаем зависимости
RUN uv venv && . .venv/bin/activate && uv pip install --no-cache .

# Копируем исходный код
COPY src ./src

# Этап выполнения
FROM python:3.13-slim

WORKDIR /frontend

# Копируем виртуальное окружение и код
COPY --from=builder /frontend /frontend

# Устанавливаем uv в финальном образе (для активации venv)
RUN pip install --no-cache-dir uv

# Активируем venv и запускаем приложение
CMD ["sh", "-c", ". .venv/bin/activate && python src/main.py"]