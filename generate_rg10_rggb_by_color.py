#!/usr/bin/env python3
"""
Usage: python generate_rg10_binary_color.py <color> <width> <height>
Generates a solid color RG10 RGGB binary image using generate_rg10_rggb.py.
"""
import sys
import subprocess

GENERATOR = 'generate_rg10_rggb_binary.py'

COLOR_MAP = {
    'grey':   (512, 512, 512),
    'gray':   (512, 512, 512),
    'red':    (1023, 0, 0),
    'green':  (0, 1023, 0),
    'blue':   (0, 0, 1023),
    'white':  (1023, 1023, 1023),
    'black':  (0, 0, 0),
    'yellow': (1023, 1023, 0),
    'magenta':(1023, 0, 1023),
}

USAGE = "Usage: python {GENERATOR} <color> <width> <height>"

def main():
    if len(sys.argv) != 4:
        print(USAGE)
        sys.exit(1)
    color = sys.argv[1].lower()
    width = sys.argv[2]
    height = sys.argv[3]
    if color not in COLOR_MAP:
        print(f"Unknown color: {color}")
        sys.exit(1)
    r, g, b = COLOR_MAP[color]
    outfile = f"{color}.rggb.raw"
    mode = "binary"  # Always binary for this script
    # Delegate to the Python RGGB generator
    cmd = [sys.executable, GENERATOR, str(r), str(g), str(b), width, height, mode, outfile]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {GENERATOR}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
