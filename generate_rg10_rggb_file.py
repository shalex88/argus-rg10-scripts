#!/usr/bin/env python3
"""
Generate a synthetic RG10 (10-bit) RGGB Bayer pattern image as a binary file.
Usage: python generate_rg10_rggb_file.py <R> <G> <B> <width> <height> <output_file>
"""
import sys
import struct

USAGE = "Usage: python generate_rg10_rggb_file.py <R> <G> <B> <width> <height> <output_file>"


def validate_color(val, name):
    if not val.isdigit():
        raise ValueError(f"{name} value must be an integer.")
    ival = int(val)
    if not (0 <= ival <= 1023):
        raise ValueError(f"{name} value must be between 0 and 1023.")
    return ival


def to_rg10_bytes(value):
    """Pack a 10-bit value into 2 bytes (little-endian, lower 2 bits in high byte)."""
    if not (0 <= value <= 1023):
        raise ValueError("Value out of 10-bit range.")
    low = value & 0xFF
    high = (value >> 8) & 0x03
    return struct.pack('<BB', low, high)


def main():
    if len(sys.argv) != 7:
        print(USAGE)
        sys.exit(1)

    try:
        R = validate_color(sys.argv[1], 'R')
        G = validate_color(sys.argv[2], 'G')
        B = validate_color(sys.argv[3], 'B')
        WIDTH = int(sys.argv[4])
        HEIGHT = int(sys.argv[5])
        outfile = sys.argv[6]
    except Exception as e:
        print(f"Error: {e}")
        print(USAGE)
        sys.exit(1)

    # Generate image data
    image_data = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # RGGB Bayer pattern
            if y % 2 == 0:
                color = R if x % 2 == 0 else G
            else:
                color = G if x % 2 == 0 else B
            image_data.extend(to_rg10_bytes(color))

    with open(outfile, 'wb') as f:
        f.write(image_data)
    print(f"RG10 RGGB binary image written to {outfile}")


if __name__ == "__main__":
    main()
