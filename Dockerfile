FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies required for some python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8501 for Streamlit
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
