FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# New test stage
FROM python:3.9-slim as tester
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN pip install pytest pytest-cov
ENV PATH=/root/.local/bin:$PATH

# Final stage remains the same
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN useradd -m appuser && \
    chown -R appuser /app && \
    chown -R appuser /home/appuser
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 5000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=2"]