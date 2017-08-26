# -*- coding: utf-8 -*-
import os
import sys
import time

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))  #

from bin.clean import recycle


if __name__ == '__main__':
    while True:
        recycle()
        time.sleep(10)
