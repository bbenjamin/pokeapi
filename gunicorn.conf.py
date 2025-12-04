# Gunicorn configuration for Railway deployment
# Optimized for Railway's 1GB memory limit

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Worker processes - conservative for Railway's memory limits
workers = 1  # Single worker to minimize memory usage
worker_class = "gthread"  # Use threaded workers instead of sync
threads = 2  # Limited threads to control memory

# Worker behavior
worker_connections = 1000
max_requests = 1000  # Restart workers after 1000 requests to prevent memory leaks
max_requests_jitter = 50
preload_app = True  # Preload for memory efficiency

# Timeouts
timeout = 30  # Shorter timeout for Railway
keepalive = 2

# Memory management
worker_tmp_dir = "/dev/shm"  # Use shared memory if available

# Logging
loglevel = "info"
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr

# Graceful handling
graceful_timeout = 30
