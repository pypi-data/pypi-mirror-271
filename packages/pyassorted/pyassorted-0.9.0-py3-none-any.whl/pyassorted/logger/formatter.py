import json
import logging
import sys


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "source": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            },
        }

        if record.exc_info:
            log_object["exception"] = {
                "type": str(record.exc_info[0]),
                "value": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        return json.dumps(log_object)


if __name__ == "__main__":
    # Create logger
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = JSONFormatter()

    # Add formatter to console_handler
    console_handler.setFormatter(formatter)

    # Add console_handler to logger
    logger.addHandler(console_handler)

    # Log some messages
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
