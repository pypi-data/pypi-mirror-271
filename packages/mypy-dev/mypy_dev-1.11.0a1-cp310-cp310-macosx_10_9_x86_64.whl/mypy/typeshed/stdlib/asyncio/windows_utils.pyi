import subprocess
import sys
from collections.abc import Callable
from types import TracebackType
from typing import Any, AnyStr, Literal
from typing_extensions import Self

if sys.platform == "win32":
    __all__ = ("pipe", "Popen", "PIPE", "PipeHandle")

    BUFSIZE: Literal[8192]
    PIPE = subprocess.PIPE
    STDOUT = subprocess.STDOUT
    def pipe(*, duplex: bool = False, overlapped: tuple[bool, bool] = (True, True), bufsize: int = 8192) -> tuple[int, int]: ...

    class PipeHandle:
        def __init__(self, handle: int) -> None: ...
        def __del__(self) -> None: ...
        def __enter__(self) -> Self: ...
        def __exit__(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None: ...
        @property
        def handle(self) -> int: ...
        def fileno(self) -> int: ...
        def close(self, *, CloseHandle: Callable[[int], object] = ...) -> None: ...

    class Popen(subprocess.Popen[AnyStr]):
        stdin: PipeHandle | None  # type: ignore[assignment]
        stdout: PipeHandle | None  # type: ignore[assignment]
        stderr: PipeHandle | None  # type: ignore[assignment]
        # For simplicity we omit the full overloaded __new__ signature of
        # subprocess.Popen. The arguments are mostly the same, but
        # subprocess.Popen takes other positional-or-keyword arguments before
        # stdin.
        def __new__(
            cls,
            args: subprocess._CMD,
            stdin: subprocess._FILE | None = ...,
            stdout: subprocess._FILE | None = ...,
            stderr: subprocess._FILE | None = ...,
            **kwds: Any,
        ) -> Self: ...
        def __init__(
            self,
            args: subprocess._CMD,
            stdin: subprocess._FILE | None = None,
            stdout: subprocess._FILE | None = None,
            stderr: subprocess._FILE | None = None,
            **kwds: Any,
        ) -> None: ...
