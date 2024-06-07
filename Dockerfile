# ------------------- Stage 1: Build Stage ------------------------------
FROM python:3.11 AS backend-builder

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the backend directory into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir pdm \
    && pdm install

# ------------------- Stage 2: Final Stage ------------------------------
# Use a slim Python 3.11 image as the final base image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the built dependencies and application from the backend-builder stage
COPY --from=backend-builder /app /app

# Ensure the binary has execution permissions
RUN chmod +x /app/binary

# Set the entrypoint
ENTRYPOINT [ "/app/binary" ]
