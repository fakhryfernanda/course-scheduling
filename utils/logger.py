import os
import logging

# Make sure the directory exists
log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)

# Configure the logger
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)