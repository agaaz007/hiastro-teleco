FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root
COPY . .
CMD ["poetry", "run", "python", "-m", "agent"] 