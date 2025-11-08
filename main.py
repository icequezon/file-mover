from src.config import load_config
from src.worker import FileMoverWorker
from src.logger import logger

import os


CONFIG_LOC = os.getenv("CONFIG_LOC", "/config/rules.yaml")


def main():
    logger.info("Hello from file-mover!")
    config = load_config(CONFIG_LOC)
    worker = FileMoverWorker(config)
    worker.run()


if __name__ == "__main__":
    main()
