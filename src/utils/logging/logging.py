"""
Various logging helpers.
--------------------------------------------------------------------------------
`src.utils.logging.logging`

"""
import os
import numpy as np


# ================================================================================
# Misc. Formatting Functions/Variables
# ================================================================================
# Colors
RED    = "\033[0;31m"
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE   = "\033[0;34m"
CYAN   = "\033[0;96m"

# Bold Text
RESET  = "\033[0m"
BOLD   = "\033[1m"
UNBOLD = "\033[22m"

# Horizontal line separators
HLINE = f"{'-'*80}"
def b(text): return f"{BOLD}{text}{RESET}"

# Output header
def print_header(text): print(f"\n{HLINE}\n{text}\n{HLINE}")

# Bold
def b(s): return f"{BOLD}{s}{RESET}"

# Quick mean (+/- std) printing
def mean_std(neg: np.array, pos: np.array):
    print(f"{b('Control:    ')} {neg.mean():6.4f} (+/- {neg.std():6.4f})  | Count: {len(neg):4}")
    print(f"{b('ProbableAD: ')} {pos.mean():6.4f} (+/- {pos.std():6.4f})  | Count: {len(pos):4}")

# --------------------------------------------------------------------------------
# Time formatting
# --------------------------------------------------------------------------------
def format_time(seconds: float | int | None) -> str:
    """ MM:SS for a number of seconds. Returns "—" if None. """
    if seconds is None: return "—"
    mins = int(seconds) // 60
    secs = int(seconds)  % 60
    return f"{mins:02d}:{secs:02d}"

