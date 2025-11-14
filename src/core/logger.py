import logging
import sys


class AppLogger:
    def __init__(self, name: str = __name__, level: int = logging.INFO):
        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            self.logger.setLevel(level)
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )

            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False

    def debug(self, msg, *a, **kw):
        self.logger.debug(msg, *a, **kw)

    def info(self, msg, *a, **kw):
        self.logger.info(msg, *a, **kw)

    def warning(self, msg, *a, **kw):
        self.logger.warning(msg, *a, **kw)

    def error(self, msg, *a, **kw):
        self.logger.error(msg, *a, **kw)

    def critical(self, msg, *a, **kw):
        self.logger.critical(msg, *a, **kw)
