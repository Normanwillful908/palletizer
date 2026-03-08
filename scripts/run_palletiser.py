#!/usr/bin/env python3
"""Launch the palletiser with the default configuration."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from palletizer_full.run import main

if __name__ == "__main__":
    main()
