FROM python:3.11

# Install only the core system libraries
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Fix the NumPy conflict immediately
RUN pip install --no-cache-dir "numpy<2.0.0"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# No pre-downloading here to prevent the build error
CMD ["python", "bot.py"]
