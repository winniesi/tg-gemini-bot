import logging

logger = logging.getLogger(__name__)


def send_log(text):
    """Log to stdout (visible in Vercel function logs)."""
    logger.info(text)


def send_image_log(text, imageID):
    """Log image to stdout."""
    logger.info(f"[image] {imageID} {text}")
