# Shoonya Wipe Development Environment
# Python 3.11 slim base with Linux disk tools
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and disk tools
RUN apt-get update && apt-get install -y \
    # Essential build tools
    build-essential \
    # Disk utilities (util-linux includes lsblk, fstrim, wipefs)
    util-linux \
    hdparm \
    nvme-cli \
    # Additional tools
    procps \
    lsof \
    # Minimal X libs for reportlab (fonts rendering)
    libxext6 \
    libxrender1 \
    libx11-6 \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 saferase && \
    mkdir -p /app/out /app/exports /app/keys /app/templates && \
    chown -R saferase:saferase /app
USER saferase

# Default to web GUI (non-destructive simulation). No device access is granted by default.
EXPOSE 5000
ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app
CMD ["python", "main.py", "web"]
