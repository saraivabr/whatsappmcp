# Python MCP Server Dockerfile
FROM python:3.11-slim

# Install FFmpeg for audio conversion support
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY *.py ./

# Install Python dependencies
RUN uv sync

# Expose any necessary ports (if needed in the future)
# EXPOSE 8000

# Set environment variable for the bridge API
ENV WHATSAPP_API_BASE_URL="http://whatsapp-bridge:8080/api"

# Run the MCP server
CMD ["uv", "run", "main.py"]
