# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# Install system dependencies for PyQt5 and X11
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    python3-pyqt5.qtcore \
    python3-pyqt5.qtgui \
    python3-pyqt5.qtwidgets \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY task_manager_qt.py .
COPY README.md .

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (if needed for future web version)
EXPOSE 8080

# Default command to run the application
CMD ["python", "task_manager_qt.py"] 