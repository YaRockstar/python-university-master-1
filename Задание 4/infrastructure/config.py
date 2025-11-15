import logging
import os
import sys

logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

logger = logging.getLogger("transport_company")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

log_file_path = os.path.join(logs_dir, "transport_company.log")
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
