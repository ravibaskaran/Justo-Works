# Odoo 18 Migration Environment
# Based on Debian 12 (Bookworm) with Python 3.11+

FROM debian:bookworm-slim

LABEL maintainer="Justo-Works Migration Team"
LABEL version="18.0"
LABEL description="Odoo 18 environment for migration from Odoo 15"

# Set shell to bash with error handling
SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    ODOO_VERSION=18.0 \
    ODOO_USER=odoo \
    ODOO_HOME=/opt/odoo

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python and build tools
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-wheel \
    python3-setuptools \
    build-essential \
    # PostgreSQL client
    postgresql-client \
    # Libraries required by Odoo
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    libpq-dev \
    # Tools
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    node-less \
    npm \
    # wkhtmltopdf dependencies
    fontconfig \
    libx11-6 \
    libxext6 \
    libxrender1 \
    xfonts-base \
    xfonts-75dpi \
    # Other utilities
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf (required for PDF reports)
RUN wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm -f wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Verify Python version (should be 3.11+)
RUN python3 --version

# Create Odoo user
RUN useradd -ms /bin/bash -d $ODOO_HOME $ODOO_USER

# Create directories
RUN mkdir -p $ODOO_HOME/odoo \
    && mkdir -p $ODOO_HOME/custom-addons \
    && mkdir -p $ODOO_HOME/data/filestore \
    && mkdir -p $ODOO_HOME/data/sessions \
    && mkdir -p $ODOO_HOME/logs \
    && chown -R $ODOO_USER:$ODOO_USER $ODOO_HOME

# Switch to odoo user
USER $ODOO_USER
WORKDIR $ODOO_HOME

# Clone Odoo 18.0
RUN git clone --depth 1 --branch 18.0 https://github.com/odoo/odoo.git $ODOO_HOME/odoo

# Install Python dependencies
COPY requirements.txt $ODOO_HOME/
RUN pip3 install --user --no-cache-dir -r requirements.txt

# Copy configuration
COPY --chown=$ODOO_USER:$ODOO_USER odoo18.conf $ODOO_HOME/odoo.conf

# Expose Odoo port
EXPOSE 8069

# Set working directory
WORKDIR $ODOO_HOME/odoo

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8069/web/health || exit 1

# Entry point
ENTRYPOINT ["/opt/odoo/odoo/odoo-bin"]

# Default command
CMD ["-c", "/opt/odoo/odoo.conf"]
