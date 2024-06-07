# ------------------- Stage 1: Build Stage ------------------------------
FROM python:3.11 AS backend-builder

    # Set the working directory to /app
WORKDIR /app
    
    # Copy the contents of the backend directory into the container at /app
COPY . /app
    
    # Install dependencies
RUN pip install --no-cache-dir pdm
RUN pdm install
    
    # ------------------- Stage 2: Final Stage ------------------------------
    
    # Use a slim Python 3.9 image as the final base image
FROM python:3.11-slim
    
    # Set the working directory to /app
WORKDIR /app
    
    # Copy the built dependencies from the backend-builder stage
COPY --from=0 /app ./binary
ENTRYPOINT [ "./binary" ]