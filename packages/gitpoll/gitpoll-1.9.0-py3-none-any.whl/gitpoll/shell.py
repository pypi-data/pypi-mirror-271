import subprocess as subproc
from subprocess import PIPE
from typing import Union as U, List, Dict
import shlex
from pyshared.python import default_repr as def_repr
from logfunc import logf

from .log import logger

class CmdResult:
    @logf(level='debug', use_logger=logger)
    def __init__(self, code: int, stdout: str, stderr: str):
        self.code, self.stdout, self.stderr = code, stdout, stderr

    def __repr__(self):
        return def_repr(self)

    def __str__(self):
        return self.__repr__()

    @property
    def status(self) -> int:
        return self.code

    @property
    def output(self) -> str:
        return self.stdout.strip()

    @property
    def error(self) -> str:
        return self.stderr.strip()


class CmdExec:
    @logf(level='debug', use_logger=logger)
    def __init__(self, cmd: U[str, List[str]]):
        self.command = shlex.split(cmd) if isinstance(cmd, str) else cmd
        self.code, self.stdout, self.stderr = 0, "", ""
        self.execute()

    @logf(level='debug', use_logger=logger)
    def execute(self) -> CmdResult:
        try:
            process = subproc.Popen(
                self.command, stdout=PIPE, stderr=PIPE, universal_newlines=True
            )
            self.stdout, self.stderr = process.communicate()
            self.code = process.returncode
        except Exception as e:
            logger.error(
                "Error executing command: {}".format(e), exc_info=True
            )
            self.code = -1
            self.stderr = "Command execution failed: {}".format(e)
        return CmdResult(self.code, self.stdout, self.stderr)

    @property
    def status(self) -> int:
        return self.code

    @property
    def output(self) -> str:
        return self.stdout.strip()

    @property
    def error(self) -> str:
        return self.stderr.strip()

    def __repr__(self):
        return def_repr(self)

    def __str__(self):
        return self.__repr__()


# Usage example:
# executor = CommandExecutor('ls -la')
# executor.execute()
# print(executor.summary())
