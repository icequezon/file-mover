from src.config import load_config
from src.worker import FileMoverWorker
from src.logger import logger


def main():
    logger.info("Hello from file-mover!")
    config = load_config("./config/rules.yaml")
    worker = FileMoverWorker(config)
    worker.run()


if __name__ == "__main__":
    main()
