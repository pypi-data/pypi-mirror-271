import os
import sys

pkg_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_path not in sys.path:
    sys.path.append(pkg_path)

from coffe_analyzer import coffeanalyzer

__version__ = "0.1.1"