# logger/evaluation.py
import os
import logging

log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)

# Define the logger object
logger = logging.getLogger('evaluation')
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.FileHandler(os.path.join(log_dir, 'evaluation.log'))
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
