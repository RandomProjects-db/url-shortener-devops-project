# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
# Copy only Go files first for better caching
COPY src/worker/go.mod src/worker/go.sum ./
RUN go mod download
# Copy remaining files
COPY src/worker/ .
RUN CGO_ENABLED=0 GOOS=linux go build -o url-shortener-worker

# Final stage
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/url-shortener-worker .
CMD ["./url-shortener-worker"]