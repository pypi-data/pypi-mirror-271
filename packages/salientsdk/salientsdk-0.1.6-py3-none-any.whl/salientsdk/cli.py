#!/usr/bin/env python

"""Command line interface for the Salient SDK.

Usage:
```
salientsdk examples
salientsdk version
```

Copyright Salient Predictions 2024
"""

import sys

from salientsdk.__main__ import main as main_logic


def main():
    """Dispatch to __main__.py."""
    main_logic()


if __name__ == "__main__":
    main()
