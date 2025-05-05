FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o url-shortener-worker

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/url-shortener-worker .
CMD ["./url-shortener-worker"]