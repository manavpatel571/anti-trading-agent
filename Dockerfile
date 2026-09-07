FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including TA-Lib requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Install Python dependencies
COPY pyproject.toml .
# Assuming pip or uv is used. Let's use pip for simplicity
RUN pip install .

COPY . .

CMD ["python", "scripts/paper_trade.py"]
