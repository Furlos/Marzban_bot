FROM python:3.13-slim
WORKDIR /frontend
RUN pip install uv
COPY ../pyproject.toml ./uv.lock ./
RUN uv sync
COPY ./src ./
CMD ["uv", "run", "python3", "main.py"]