"""
Centralized Cloud Logging setup.

- Uses CloudLoggingHandler (background thread) so logging does not add latency
  to your request path.
- Keeps the JSON shape you’ve been using:
  jsonPayload.message + jsonPayload.custom{...}
"""

import os
from typing import Optional, Dict

import logging
from google.cloud import logging as cloud_logging
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

def _setup_logger() -> logging.Logger:
    """Create or return the singleton evaluation logger."""
    log_name = "authentication-logs"


    try:
        client = cloud_logging.Client()
        client.setup_logging()
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

    except Exception as e:
        # Fallback to console if Cloud Logging is unavailable (local dev)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(log_name)
        logger.warning("Cloud Logging setup failed; using console. Error: %s", e)

    return logger


_eval_log = _setup_logger()


# Modified log_structured_entry function
def log_structured_entry(message: str, severity: str, custom_log: Optional[Dict] = None) -> None:
    """
    Emit a JSON-structured log row compatible with your existing queries.
    """
    try:
        structured_data = {
            "user_id": "12345",
            "event": "agent_event",
            "meta": custom_log or {}
        }
        _eval_log.info(message, extra={"json_fields": structured_data})
    except Exception as e:
        logging.error("Failed to log structured entry: %s", e)
