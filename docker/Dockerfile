FROM python:3.13-slim

WORKDIR /app

# Установка uv для управления зависимостями
RUN pip install --no-cache-dir uv

# Копируем файлы проекта
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY migrations ./migrations

# Устанавливаем зависимости
RUN uv sync --no-dev

# Создаем директорию для логов
RUN mkdir -p /var/log/blog

# Экспонируем порт
EXPOSE 8000

# Команда запуска
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

