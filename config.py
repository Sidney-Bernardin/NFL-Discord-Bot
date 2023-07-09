import os
import logging
import logging.handlers


formatter = logging.Formatter(
    "({asctime}) [{levelname}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)

# Create a logging handler to write INFO level logs to stdout.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Create a logging handler to write DEBUG level logs to .log files.
file_handler = logging.handlers.RotatingFileHandler(
    filename="logs/debug.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,
    backupCount=5,
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Configure the logger.
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        stream_handler,
        file_handler,
    ],
)

config: dict[str, str] = {
    "TOKEN": "",
    "PREFIX": "",
}

# Sets the configuration's fields from environment variables.
for key, value in config.items():
    if (new_value := os.environ.get(key)) is None:
        logging.error(f"Couldn't find environment variable '{key}'")
        exit(os.EX_CONFIG)

    config[key] = new_value
