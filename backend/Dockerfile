FROM python:3.11-slim as builder
RUN pip install uv
WORKDIR /app
COPY pyproject.toml .
RUN uv sync --no-dev

FROM python:3.11-slim
RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app/ /app/app/
COPY migrations/ /app/migrations/
RUN mkdir /app/uploads && chown -R appuser:appuser /app
USER appuser
EXPOSE 6100
ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6100"]
