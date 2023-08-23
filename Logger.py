#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


class Logger:
    """
    Třída pro nastavení loggingu.
    """

    def init(self, name, log_file):
        self = logging.getLogger(name)
        self.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                                      datefmt='%d-%b-%y %H:%M:%S')

        file_handler = logging.FileHandler(os.path.join(dir_path, log_file))
        file_handler.setFormatter(formatter)

        self.addHandler(file_handler)
        return self