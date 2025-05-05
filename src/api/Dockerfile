# Builder stage
FROM python:3.12-alpine as builder
RUN apk add --no-cache gcc musl-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Tester stage
FROM python:3.12-alpine as tester
RUN apk add --no-cache curl
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
RUN pip install --no-cache-dir pytest pytest-cov
ENV PATH="/usr/local/bin:$PATH"

# Final stage
FROM python:3.12-alpine
RUN apk add --no-cache curl
LABEL maintainer="Fahed" \
      description="URL Shortener API Service" \
      version="1.0.0"
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
RUN adduser -D appuser && \
    chown -R appuser /app
USER appuser
ENV PATH="/usr/local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=2"]