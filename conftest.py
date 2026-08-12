"""
Root conftest.py - ensures the project root is on sys.path so
'import toolkit' works when running plain "pytest" from any directory.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
