# tipos funcionais do projeto
from src.core.either import Either, Left, Right, bind, map_right, match
from src.core.option import Nothing, Option, Some, from_nullable, get_or_default
from src.core.error_result import ErrorResult, ValidationBuilder
from src.core.specification import AndSpec, NotSpec, OrSpec, Specification
from src.core.railway import tap, tap_async, then, then_async, try_catch, try_catch_async
from src.core.pipe import Pipe, AsyncPipe, pipe, async_pipe
from src.core.result import Result, Success, Failure, success, failure
from src.core.try_monad import Try, TrySuccess, TryFailure, try_of, try_of_async, to_either
from src.core.logger import logger, get_logger, setup_logger, info, debug, warning, error

__all__ = [
    # Either
    "Either",
    "Left",
    "Right",
    "match",
    "map_right",
    "bind",
    # Option
    "Option",
    "Some",
    "Nothing",
    "from_nullable",
    "get_or_default",
    # ErrorResult
    "ErrorResult",
    "ValidationBuilder",
    # Specification
    "Specification",
    "AndSpec",
    "OrSpec",
    "NotSpec",
    # Railway
    "then",
    "then_async",
    "tap",
    "tap_async",
    "try_catch",
    "try_catch_async",
    # Pipe
    "Pipe",
    "AsyncPipe",
    "pipe",
    "async_pipe",
    # Result
    "Result",
    "Success",
    "Failure",
    "success",
    "failure",
    # Try
    "Try",
    "TrySuccess",
    "TryFailure",
    "try_of",
    "try_of_async",
    "to_either",
    # Logger
    "logger",
    "get_logger",
    "setup_logger",
    "info",
    "debug",
    "warning",
    "error",
]

