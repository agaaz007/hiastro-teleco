FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root
COPY . .
EXPOSE 443
CMD ["poetry", "run", "uvicorn", "pipeline:app", "--host", "0.0.0.0", "--port", "443"] 