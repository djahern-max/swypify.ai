# Stage 1: Build the dependencies in a separate stage
FROM python:3.12-slim as builder

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev

# Install Python dependencies in a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy the application and run it
FROM python:3.12-slim

WORKDIR /usr/src/app

# Copy virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure virtual environment is used
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
COPY . .

# Default command to run the FastAPI app (override with Compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




