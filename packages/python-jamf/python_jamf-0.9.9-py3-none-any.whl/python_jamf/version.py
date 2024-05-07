#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import os
import re

__all__ = ("string", "jamf_version_up_to")


def string():
    try:
        with open(os.path.dirname(__file__) + "/VERSION", "r", encoding="utf-8") as fh:
            version = fh.read().strip()
            if version:
                return version
    except:
        pass
    return "0.0.0"


def jamf_version_up_to(min_version):
    full_version = string()
    try:
        m = re.match(r"^([0-9]+\.[0-9]+\.[0-9]+)", full_version)
        min1 = tuple(map(int, (min_version.split("."))))
        cur = tuple(map(int, (m.group(1).split("."))))
        if min1 <= cur:
            return min_version  # Pass
    except AttributeError:
        return full_version  # Fail
    return full_version  # Fail
