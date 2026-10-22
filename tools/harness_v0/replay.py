"""Replay captured observations to the unchanged recompute-kit reporter grader."""
from pathlib import Path
import sys

if __name__ == '__main__':
    sys.stdout.buffer.write(Path(sys.argv[1]).read_bytes())
