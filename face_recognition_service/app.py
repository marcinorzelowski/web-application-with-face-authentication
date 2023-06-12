import logging

from flask import Flask
from apis import api


app = Flask(__name__)
api.init_app(app)


# Set up logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

# Root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)


if __name__ == '__main__':
    app.run(debug=True)
