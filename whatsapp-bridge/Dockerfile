# Multi-stage build for WhatsApp Bridge
FROM golang:1.24.1-alpine AS builder

# Install build dependencies for CGO and SQLite
RUN apk add --no-cache gcc musl-dev sqlite-dev

# Set working directory
WORKDIR /app

# Copy go module files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY main.go ./

# Build the application with CGO enabled
ENV CGO_ENABLED=1
RUN go build -o whatsapp-bridge main.go

# Final stage
FROM alpine:latest

# Install runtime dependencies
RUN apk add --no-cache sqlite-libs ca-certificates

# Create app directory
WORKDIR /app

# Create store directory for persistent data
RUN mkdir -p /app/store

# Copy binary from builder
COPY --from=builder /app/whatsapp-bridge .

# Expose API port
EXPOSE 8080

# Run the application
CMD ["./whatsapp-bridge"]
