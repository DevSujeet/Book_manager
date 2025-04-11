import logging
import sys
import json
import httpx
from logging import StreamHandler

# Example settings dictionary (Declared First)
# This can be moved to a separate settings file.
settings = {
    "LOG_LEVEL": "DEBUG",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    "JSON_LOGGING": False,  # Set to True for structured JSON logs (Splunk preferred)
    "SPLUNK_ENABLED": False ,  # Toggle Splunk logging
    "SPLUNK_URL": "http://your-splunk-server:8088",  # Replace with actual Splunk HEC URL
    "SPLUNK_TOKEN": "your-splunk-token",  # Replace with actual Splunk HEC token
    "SPLUNK_INDEX": "fastapi_logs"
}

# Function to fetch log level from settings
def get_log_level(settings):
    return getattr(logging, settings.get("LOG_LEVEL", "DEBUG").upper(), logging.DEBUG)

# Function to determine log format
def get_formatter(json_logging=False):
    if json_logging:
        return logging.Formatter(
            json.dumps({
                "timestamp": "%(asctime)s",
                "logger": "%(name)s",
                "level": "%(levelname)s",
                "message": "%(message)s",
                "function": "%(funcName)s",
                "path": "%(pathname)s"
            }),
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        return logging.Formatter(
            "\n%(asctime)s | %(name)s | %(levelname)s | %(message)s\n[Function: %(funcName)s] [Path: %(pathname)s]",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

# Custom Splunk HEC Handler supporting both JSON & Plain Text
class SplunkHECHandler(logging.Handler):
    def __init__(self, splunk_url, token, index="main", json_logging=True):
        super().__init__()
        self.splunk_url = f"{splunk_url}/services/collector"
        self.token = token
        self.index = index
        self.json_logging = json_logging  # Determines log format

    def emit(self, record):
        log_entry = self.format(record)
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type": "application/json"
        }
        
        # Prepare data payload for Splunk
        data = {
            "event": log_entry if self.json_logging else {"message": log_entry},  # Sends as JSON if enabled
            "index": self.index,
            "sourcetype": "_json" if self.json_logging else "_raw"  # Different sourcetype for plain text
        }
        
        try:
            with httpx.Client(timeout=5.0) as client:  # Synchronous HTTP call
                response = client.post(self.splunk_url, headers=headers, json=data)
                if response.status_code not in [200, 201, 202]:
                    print(f"Failed to send log to Splunk: {response.text}")
        except httpx.RequestError as e:
            print(f"Splunk logging error: {e}")

# Function to configure logging
def configure_logging(settings):
    logger = logging.getLogger("fastapi_logger")
    logger.setLevel(get_log_level(settings))

    # Clear existing handlers before adding new ones
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler
    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(get_formatter(json_logging=settings.get("JSON_LOGGING", False)))
    logger.addHandler(stream_handler)

    # Splunk HEC Handler (if enabled)
    if settings.get("SPLUNK_ENABLED", False):
        splunk_handler = SplunkHECHandler(
            splunk_url=settings.get("SPLUNK_URL"),
            token=settings.get("SPLUNK_TOKEN"),
            index=settings.get("SPLUNK_INDEX", "main"),
            json_logging=settings.get("JSON_LOGGING", False)  # Control JSON formatting
        )
        splunk_handler.setLevel(logging.INFO)
        # splunk_handler.setFormatter(get_formatter(json_logging=settings.get("JSON_LOGGING", False)))
        splunk_handler.setFormatter(get_formatter(json_logging=True))  # Always use JSON for Splunk
        logger.addHandler(splunk_handler)

    return logger

# Initialize logger AFTER declaring settings
logger = configure_logging(settings)