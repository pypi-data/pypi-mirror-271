import os
import platform
import subprocess
import sys
import threading
from typing import Optional

from hbox.logger import get_logger

log = get_logger(__name__)


def reader(pipe, func):
    for line in iter(pipe.readline, b''):
        func(line.decode())


def execute_in_shell(command, can_be_interactive):
    stdin_pipe = subprocess.PIPE if can_be_interactive else None
    process = subprocess.Popen(' '.join(command), shell=True, stdin=stdin_pipe,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def execute_in_subprocess(command, can_be_interactive):
    stdin_pipe = subprocess.PIPE if can_be_interactive else None
    process = subprocess.Popen(command, stdin=stdin_pipe, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process


def execute_command(command, can_be_interactive: bool = False) -> Optional[int]:
    command_execution_func = execute_in_shell if platform.system().lower() == "linux" else execute_in_subprocess
    process = None
    stdin_data = None
    return_code = -1

    if can_be_interactive:
        if not sys.stdin.isatty():
            stdin_data = sys.stdin.read()
        if stdin_data:
            command.insert(2, "-i")

    try:
        log.debug(f"Running command: {' '.join(command)}")

        process = command_execution_func(command, can_be_interactive)

        if can_be_interactive and stdin_data:
            process.stdin.write(stdin_data.encode())
            process.stdin.close()

        out_thread = threading.Thread(target=reader, args=[process.stdout, sys.stdout.write])
        err_thread = threading.Thread(target=reader, args=[process.stderr, sys.stderr.write])
        out_thread.start()
        err_thread.start()
        out_thread.join()
        err_thread.join()

        return_code = process.wait()
    except (subprocess.SubprocessError, OSError) as e:
        log.debug(f"Error executing command: {e}")
        return None
    except KeyboardInterrupt:
        log.debug("Interrupted by user")
        return None
    finally:
        if process and can_be_interactive and stdin_data:
            process.stdin.close()
        return return_code


def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))
