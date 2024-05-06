"""The system purpose utilities."""

from subprocess import PIPE, run
from typing import Optional, Sequence

__all__ = ["execute"]


DEFAULT_EXECUTE_TIMEOUT: int = 30


def execute(
    args: Sequence[str],
    *,
    input: Optional[str] = None,
    timeout: int = DEFAULT_EXECUTE_TIMEOUT,
    **kwargs,
) -> tuple[Optional[str], Optional[str]]:
    """Execute command into external process.

    Args:
        args: List of the lines with the command and her options.
        input: A data string that should be sent to input stream of command.
        timeout: Command completion timeout (30 seconds by default).
        *kwargs: Additional options for subprocess.run.

    Returns:
        Two-element tuple with data from standard streams: stdout and stderr.

    Example::

        from pure_utils.system import execute

        result, _ = execute(["uname", "-o"])
        print(result.decode())
        >>> Darwin
    """
    process = run(args, stdout=PIPE, stderr=PIPE, input=input, timeout=timeout, **kwargs)
    return process.stdout, process.stderr
