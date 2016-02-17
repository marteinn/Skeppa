#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import fabric.main


def main():
    # Supply default fabricrc (if one does not exist)
    if "-c" not in sys.argv:
        rc_files = ("skeppa.env", "fabricrc.txt", ".fabricrc")

        for path in rc_files:
            if os.path.exists(path):
                sys.argv.extend(("-c", path))
                print('Loading vars from {0}'.format(path))
                break

    path = os.path.dirname(os.path.abspath(__file__))
    fabric.main.main([os.path.join(path, '../main.py')])


if __name__ == '__main__':
    main()
