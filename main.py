#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the output directory.

Stdlib-only entrypoint for the make.fun news-image entry. The image is
rendered at build time and committed next to this script, so at run time
there is nothing to draw: we only validate the file and copy it to
$MAKEFUN_OUTPUT_DIR (default /output). This runs in the grader's pinned
image, which ships no third-party packages.
"""

import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    """Return (width, height) from the PNG IHDR chunk, or None if invalid."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 24 or head[:8] != PNG_MAGIC:
        return None
    if head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def ends_with_iend(path):
    """True when the last 12 bytes form a complete IEND chunk."""
    with open(path, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    return len(tail) == 12 and tail[4:8] == b"IEND"


def fail(message):
    print(message, file=sys.stderr)
    return 1


def main():
    if not os.path.isfile(SRC):
        return fail("entry.png not found next to main.py")
    dims = png_dimensions(SRC)
    if dims is None:
        return fail("entry.png is not a valid PNG file")
    width, height = dims
    if width > MAX_DIM or height > MAX_DIM:
        return fail("entry.png is %dx%d, over the 1024x1024 limit" % (width, height))
    nbytes = os.path.getsize(SRC)
    if nbytes > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % nbytes)
    if not ends_with_iend(SRC):
        return fail("entry.png is truncated (no IEND chunk)")
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) != nbytes:
        return fail("copy to %s is incomplete" % dst)
    print("copied entry.png (%dx%d, %d bytes) to %s" % (width, height, nbytes, OUT_DIR))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
