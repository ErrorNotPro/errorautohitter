FROM python:3.11-slim

# Install high-performance system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip for faster installs
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PRE-DOWNLOAD THE MODEL (Crucial for 1-5 second startup)
# This puts the 176MB model into the Docker image so it's ready INSTANTLY.
RUN python -c "from rembg import new_session; new_session('u2net')"

COPY . .

# Set Railway to use more threads if available
ENV OMP_NUM_THREADS=4

CMD ["python", "bot.py"]
