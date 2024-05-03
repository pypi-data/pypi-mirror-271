import logging
import sys

from typing import Optional
from contextlib import suppress

from config import config

from app import app


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)
if logging.root.level > logging.DEBUG:
    # prevents log spam from infinite polling
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # somehow pydantic raises an attribute error when I'm trying to access config.Config for the type hint
    # removing the type hint solves the issue, but I'd rather just suppress the pydantic error
    with suppress(AttributeError):
        config: Optional[config.Config] = config.load_config()
    if not config:
        logger.error("Couldn't load config file")
        sys.exit(1)

    app = app.App(config)

    app.run()
