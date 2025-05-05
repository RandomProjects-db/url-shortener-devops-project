# Builder stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
# Upgrade pip and setuptools globally (not just --user)
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Tester stage
FROM python:3.9-slim as tester
WORKDIR /app
# Upgrade pip and setuptools globally here too
RUN pip install --no-cache-dir --upgrade pip setuptools
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
RUN pip install --no-cache-dir pytest pytest-cov
ENV PATH="/usr/local/bin:$PATH"

# Final stage (for production API container)
FROM python:3.9-slim
WORKDIR /app
# Upgrade pip and setuptools globally in the final image
RUN pip install --no-cache-dir --upgrade pip setuptools
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
RUN useradd -m appuser && \
    chown -R appuser /app && \
    chown -R appuser /home/appuser
USER appuser
ENV PATH="/usr/local/bin:$PATH"
EXPOSE 5000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=2"]