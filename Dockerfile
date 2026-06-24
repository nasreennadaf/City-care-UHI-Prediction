# Stage 1: Build the React Application
FROM node:18-alpine AS build
# Set the working directory for the frontend build
WORKDIR /app/frontend

# 1. Copy package files from the frontend subdirectory
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

# 2. Copy the rest of the frontend source (src, public, etc.)
COPY frontend/ ./

# 3. Build the React app
RUN npm run build

# Stage 2: Build the Python Flask Application
FROM python:3.9-slim
WORKDIR /app

# Install system dependencies for scientific/ML packages
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 4. Install Backend Dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy backend source code
COPY backend/ ./backend/

# 6. Copy React build output from Stage 1
# Note: Since WORKDIR was /app/frontend, the output is in /app/frontend/build
COPY --from=build /app/frontend/build ./build

# Set environment to run from the backend directory
WORKDIR /app/backend

# Use Gunicorn for production deployment
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app