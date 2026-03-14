FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pin NumPy immediately before installing anything else
RUN pip install --no-cache-dir "numpy<2.0.0"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# This line should now succeed without the NumPy error
RUN python -c "from rembg import new_session; new_session('u2netp')"

COPY . .

CMD ["python", "bot.py"]
