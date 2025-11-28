# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# instala dependencias de build
RUN pip install --no-cache-dir --upgrade pip

# copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# cria usuario nao-root
RUN useradd --create-home --shell /bin/bash app
USER app

# copia dependencias do builder
COPY --from=builder /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# copia codigo
COPY --chown=app:app src/ ./src/
COPY --chown=app:app main.py .

# configuracoes
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

# healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "main.py"]

