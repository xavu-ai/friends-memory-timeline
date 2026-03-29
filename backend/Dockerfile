FROM python:3.11-slim as builder
RUN pip install uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

FROM python:3.11-slim
RUN useradd -m --uid=1000 appuser
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app/ /app/app/
ENV PYTHONPATH=/app
USER appuser
EXPOSE 6100
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:6100/healthz')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6100"]
