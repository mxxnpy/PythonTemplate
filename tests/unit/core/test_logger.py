"""
Tests for Logger
"""

from __future__ import annotations

import logging
import pytest

from src.core.logger import (
    ColoredFormatter,
    SimpleFormatter,
    get_logger,
    setup_logger,
)


class TestLogger:
    """testes para logger"""

    def test_setup_logger_returns_logger(self) -> None:
        log = setup_logger("test_setup")
        assert isinstance(log, logging.Logger)
        assert log.name == "test_setup"

    def test_get_logger_returns_same_instance(self) -> None:
        log1 = get_logger("test_same")
        log2 = get_logger("test_same")
        assert log1 is log2

    def test_logger_has_console_handler(self) -> None:
        log = setup_logger("test_handlers")
        assert len(log.handlers) >= 1
        assert any(isinstance(h, logging.StreamHandler) for h in log.handlers)

    def test_logger_with_file_handler(self, tmp_path) -> None:
        log_file = tmp_path / "test.log"
        log = setup_logger("test_file", log_file=str(log_file))

        assert len(log.handlers) == 2
        assert any(isinstance(h, logging.FileHandler) for h in log.handlers)

    def test_colored_formatter_formats_message(self) -> None:
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test message" in formatted
        assert "INFO" in formatted

    def test_simple_formatter_formats_message(self) -> None:
        formatter = SimpleFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Error message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Error message" in formatted
        assert "ERROR" in formatted
        assert "test" in formatted

    def test_logger_level_setting(self) -> None:
        log = setup_logger("test_level", level="DEBUG")
        assert log.level == logging.DEBUG

        log2 = setup_logger("test_level2", level="ERROR")
        assert log2.level == logging.ERROR

