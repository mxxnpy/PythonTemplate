"""
Logger - handler universal com cores
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from typing import Literal

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


# cores por nivel
LEVEL_COLORS = {
    "DEBUG": Fore.CYAN if COLORAMA_AVAILABLE else "",
    "INFO": Fore.GREEN if COLORAMA_AVAILABLE else "",
    "WARNING": Fore.YELLOW if COLORAMA_AVAILABLE else "",
    "ERROR": Fore.RED if COLORAMA_AVAILABLE else "",
    "CRITICAL": Fore.RED + Style.BRIGHT if COLORAMA_AVAILABLE else "",
}

RESET = Style.RESET_ALL if COLORAMA_AVAILABLE else ""
DIM = Style.DIM if COLORAMA_AVAILABLE else ""
BRIGHT = Style.BRIGHT if COLORAMA_AVAILABLE else ""


class ColoredFormatter(logging.Formatter):
    """formatter com cores"""

    def __init__(self, fmt: str | None = None, datefmt: str | None = None):
        super().__init__(fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:
        # cor do nivel
        level_color = LEVEL_COLORS.get(record.levelname, "")

        # formata timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

        # formata nome do modulo (curto)
        module = record.name.split(".")[-1][:15].ljust(15)

        # monta mensagem
        level = record.levelname.ljust(8)
        msg = record.getMessage()

        # adiciona exception se houver
        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)

        return (
            f"{DIM}{timestamp}{RESET} "
            f"{level_color}{level}{RESET} "
            f"{DIM}{module}{RESET} "
            f"{msg}"
        )


class SimpleFormatter(logging.Formatter):
    """formatter simples sem cores (para arquivos)"""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname.ljust(8)
        module = record.name
        msg = record.getMessage()

        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)

        return f"{timestamp} {level} {module} - {msg}"


def setup_logger(
    name: str = "app",
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO",
    log_file: str | None = None,
) -> logging.Logger:
    """configura e retorna logger"""

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    logger.handlers.clear()

    # console handler (com cores)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    # file handler (sem cores)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(SimpleFormatter())
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "app") -> logging.Logger:
    """retorna logger existente ou cria novo"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# logger padrao da aplicacao
logger = setup_logger("app")


# funcoes de conveniencia
def debug(msg: str, *args, **kwargs) -> None:
    logger.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    logger.info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    logger.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    logger.error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs) -> None:
    logger.critical(msg, *args, **kwargs)


def exception(msg: str, *args, **kwargs) -> None:
    logger.exception(msg, *args, **kwargs)