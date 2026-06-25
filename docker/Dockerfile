# Use python:3.13-slim as the base image
FROM python:3.13-slim

# Install git because the project has a dependency on a git repository (mini)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the uv binary for fast package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the dependency specification files
COPY pyproject.toml uv.lock ./

# Install dependencies, including fastapi and uvicorn which are required for server.py
RUN uv pip install --system -r pyproject.toml fastapi uvicorn

# Copy the server script
COPY server.py ./

# Expose the application port
EXPOSE 8000

# Start the uvicorn server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
