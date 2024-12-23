FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    gnupg \
    unzip \
    git \
    libzip-dev \
    libpng-dev \
    libffi-dev \
    libssl-dev \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libglib2.0-0 \
    libfontconfig1 \
    libpango1.0-0 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libxss1 \
    libnss3-tools \
    lsb-release \
    --no-install-recommends

# add google repository and install chrome_driver
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable chromium-driver

# install pack selnium and config virtual environment
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir selenium

# install php extensions
RUN docker-php-ext-install pdo

# Instalar Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# add path to virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set config to chrome selenium and permissions
RUN mkdir -p /home/chrome && chmod -R 777 /home/chrome
ENV TMPDIR=/home/chrome

# clean cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# work path
WORKDIR /app