#!/usr/bin/env python

import errno
import signal
import sys
from argparse import ArgumentParser
from multiprocessing import Process
from multiprocessing import Queue
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from src.client import client
from src.server import server


def exit_on_sigint(number, stack_frame):
    """
    Custom handler that just exits the process if there is a SIGINT

    There are several processes/threads that will be spawned, so install this
    handler as early as possible so that others inherit it. Otherwise, each
    thread/process will produce their own traceback output which will all be
    dumped together to console.
    """
    QApplication.quit()
    sys.exit(errno.EOWNERDEAD)  # 130


class TDefaults:
    """Hold various default configuration parameters"""

    config_path = str(Path(Path.home(), ".config", "tslot"))
    config_file = str(Path(config_path, "config.yml"))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_on_sigint)

    ap = ArgumentParser(description="Make time-driven decision")

    ap.add_argument(
        "--profile",
        type=str,
        nargs="?",
        choices=["personal", "developer"],
        default="personal",
        help="""
            Select developer profile to use default config and database. This
            does not change your personal data.
        """,
    )

    ap.add_argument(
        "--config",
        "--config-file",
        type=str,
        nargs="?",
        default=TDefaults.config_file,
        help="Path to your configuration file.",
    )

    ap.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="Write more output to console.",
    )

    ap.add_argument(
        "--silent",
        action="store_true",
        default=False,
        help="Silence all console output.",
    )

    args = ap.parse_args()

    client_to_server_messages = Queue()
    server_to_client_messages = Queue()

    # Start the server process in a separate process
    server_process = Process(
        target=server, args=(client_to_server_messages, server_to_client_messages)
    )
    server_process.start()

    # Start the client process here, in the main process, because Qt expects
    # it this way. This blocks the main process until the client terminates
    client(server_to_client_messages, client_to_server_messages)

    # Client process terminated, so terminate the server as well
    server_process.terminate()
    server_process.join()
