# Builder stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
# Upgrade pip and setuptools globally (not just --user)
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Tester stage
FROM python:3.12-slim as tester
WORKDIR /app
# Upgrade pip and setuptools globally here too
RUN pip install --no-cache-dir --upgrade pip setuptools
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
RUN pip install --no-cache-dir pytest pytest-cov
ENV PATH="/usr/local/bin:$PATH"

# Final stage (for production API container)
FROM python:3.12-slim
LABEL maintainer="Fahed" \
      description="URL Shortener API Service" \
      version="1.0.0"
WORKDIR /app
# Upgrade pip and setuptools globally in the final image
RUN pip install --no-cache-dir --upgrade pip setuptools
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
RUN useradd -m appuser && \
    chown -R appuser /app && \
    chown -R appuser /home/appuser
USER appuser
ENV PATH="/usr/local/bin:$PATH"
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1
  ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1
  CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=2"]