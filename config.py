"""
Configuration settings for SMS API Service
"""

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG_MODE = True

# Worker Settings
# Worker Settings
MAX_WORKERS = 500  # Extreme mode: 500 parallel workers
REQUEST_TIMEOUT = 10  # Giam timeout xuong 10s de fail nhanh thi chuyen sang service khac

# Rate Limiting (optional)
RATE_LIMIT_ENABLED = False
RATE_LIMIT_CALLS = 100  # Số requests tối đa
RATE_LIMIT_PERIOD = 60  # Trong khoảng thời gian (giây)

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Services
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICES_DIR = os.path.join(BASE_DIR, "services")
# Fix path for Vercel/Python import system
if 'services' not in SERVICES_DIR:
    SERVICES_DIR = "services"
SERVICE_FILES = [
    "smsvip_0",
    "smsvip_1", 
    "smsvip_2",
    "smsvip_3",
    "smsvip_4"
]
