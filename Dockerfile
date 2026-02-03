FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set execute permission for start script
RUN chmod +x start.sh && \
    apt-get update && \
    apt-get install -y dos2unix && \
    dos2unix start.sh && \
    apt-get clean

# Entrypoint using start script
CMD ["./start.sh"]
