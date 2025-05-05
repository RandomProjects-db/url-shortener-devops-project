# Stage 1: Build dependencies
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Security: Run as non-root user
RUN useradd -m appuser && \
    chown -R appuser /app && \
    chown -R appuser /home/appuser
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 5050
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=2"]