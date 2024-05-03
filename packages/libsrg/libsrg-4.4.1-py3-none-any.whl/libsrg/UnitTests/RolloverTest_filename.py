#!/usr/bin/env  python3

from pathlib import Path

from libsrg.LoggingAppBase import LoggingAppBase
from libsrg.LoggingCounter import LoggingCounter
from libsrg.Runner import Runner


class SampleApp(LoggingAppBase):
    """
    This app is intended to test logging file rollover

    Legacy supported filename as part of constructor args,
    Legacy ALSO supported logfile attached after arg parse

    """

    def __init__(self):
        filename = "/tmp/roll_log.log"
        fp = Path(filename)

        pargs = {"description": "This is an example application", }
        LoggingAppBase.__init__(self, parser_args=pargs, filename=filename, maxBytes=20000)
        # invoke the parser
        self.perform_parse()
        #
        self.logger.info(f"after parsing {self.args}")

    def log_loop(self, n=1000):
        for i in range(n):
            self.logger.info(f"log {i} of {n}")

    @classmethod
    def demo(cls):
        app = SampleApp()
        app.log_loop(1000)
        LoggingCounter.rotate_files()
        app.log_loop(2000)
        LoggingCounter.rotate_files()
        r = Runner(["bash", "-c", "ls -l /tmp/roll_log*"])
        for line in r.so_lines:
            app.logger.info(line)


if __name__ == '__main__':
    SampleApp.demo()
