import logging

import uvicorn

from pyfuta import config
from pyfuta.app.logging import Ansi, log
from pyfuta.app.entrypoint import pyfuta_app


if __name__ == "__main__":
    log(f"Uvicorn running on http://{config.bind_address}:{str(config.bind_port)} (Press CTRL+C to quit)", Ansi.YELLOW)
    uvicorn.run(pyfuta_app, log_level=logging.WARNING, port=config.bind_port, host=config.bind_address)
