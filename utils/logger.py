"""
============================================================
Universal Logger
============================================================

Provides uniform logging across all modules.

Supports

✓ INFO
✓ WARNING
✓ ERROR
✓ SUCCESS

============================================================
"""

import os
import logging
from datetime import datetime


class Logger:

    def __init__(self, log_directory="generated/reports"):

        os.makedirs(log_directory, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.log_file = os.path.join(
            log_directory,
            f"framework_{timestamp}.log"
        )

        logging.basicConfig(

            filename=self.log_file,

            level=logging.INFO,

            format="%(asctime)s | %(levelname)s | %(message)s",

            datefmt="%Y-%m-%d %H:%M:%S"

        )

    # -----------------------------------------------------

    def info(self, message):

        print(f"[INFO] {message}")

        logging.info(message)

    # -----------------------------------------------------

    def warning(self, message):

        print(f"[WARNING] {message}")

        logging.warning(message)

    # -----------------------------------------------------

    def error(self, message):

        print(f"[ERROR] {message}")

        logging.error(message)

    # -----------------------------------------------------

    def success(self, message):

        print(f"[SUCCESS] {message}")

        logging.info(f"SUCCESS : {message}")

    # -----------------------------------------------------

    def separator(self):

        print("=" * 70)

        logging.info("=" * 70)

    # -----------------------------------------------------

    def section(self, title):

        print("\n" + "=" * 70)

        print(title)

        print("=" * 70)

        logging.info("=" * 70)

        logging.info(title)

        logging.info("=" * 70)