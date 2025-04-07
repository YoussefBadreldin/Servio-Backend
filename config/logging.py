import logging
from pathlib import Path
from ..config.settings import settings

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.DATA_DIR / "servio.log"),
            logging.StreamHandler()
        ]
    )
    
    # Suppress noisy logs
    for logger_name in ["httpx", "github3", "urllib3"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)