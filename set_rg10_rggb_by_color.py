#!/usr/bin/env python3
import sys
import subprocess

GENRATOR = 'generate_rg10_rggb_file.py'
CAMERA = 'config_camera_rg10_rggb_output.py'

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

USAGE = f"""Usage:
For binary mode: python {sys.argv[0]} binary <color> <width> <height>
For camera mode: python {sys.argv[0]} camera <color>"""

def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode not in ["binary", "camera"]:
        print(f"Invalid mode: {mode}. Mode must be 'binary' or 'camera'")
        print(USAGE)
        sys.exit(1)

    color = sys.argv[2].lower()
    if color not in COLOR_MAP:
        print(f"Unknown color: {color}")
        print("Available colors:", ", ".join(sorted(COLOR_MAP.keys())))
        sys.exit(1)

    r, g, b = COLOR_MAP[color]
    outfile = f"{color}.rggb.raw"

    if mode == "binary":
        if len(sys.argv) != 5:
            print("Binary mode requires width and height parameters")
            print(USAGE)
            sys.exit(1)
        width = sys.argv[3]
        height = sys.argv[4]
        cmd = [sys.executable, GENRATOR, str(r), str(g), str(b), width, height, outfile]
    else:  # camera mode
        if len(sys.argv) != 3:
            print("Camera mode only requires color parameter")
            print(USAGE)
            sys.exit(1)
        cmd = [sys.executable, CAMERA, str(r), str(g), str(b)]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
