# Builder stage
FROM python:3.12-alpine as builder
RUN apk update && apk upgrade
RUN apk add --no-cache gcc musl-dev nasm make
WORKDIR /app

# Copy entire project context
COPY . .

# Build ASM library
RUN cd src/asm && \
    make clean && \
    make && \
    cp libhash.so /usr/local/lib/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r src/api/requirements.txt
RUN pip install --no-cache-dir gunicorn  # Explicitly install gunicorn

# Tester stage - Use a different base image than the builder
FROM python:3.12-alpine as tester
RUN apk update && apk upgrade
RUN apk add --no-cache curl
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/lib/libhash.so /usr/local/lib/
COPY . .
# Install test dependencies directly
RUN pip install --no-cache-dir pytest pytest-cov
ENV PYTHONPATH=/app:$PYTHONPATH \
    PATH="/usr/bin:/usr/local/bin:$PATH" \
    LD_LIBRARY_PATH="/usr/local/lib"
# No CMD - docker-compose provides the command

# Final stage
FROM python:3.12-alpine
RUN apk update && apk upgrade
RUN apk add --no-cache curl
LABEL maintainer="Fahed" \
      description="URL Shortener API Service" \
      version="1.0.0"
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/libhash.so /usr/local/lib/
COPY . .
# Create user and avoid extra gunicorn install since we already copied site-packages
RUN adduser -D appuser && \
    chown -R appuser /app
USER appuser
ENV PATH="/usr/local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LD_LIBRARY_PATH="/usr/local/lib"
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1
CMD ["gunicorn", "--chdir", "src/api", "app:app", "-b", "0.0.0.0:5000", "--workers=2"]