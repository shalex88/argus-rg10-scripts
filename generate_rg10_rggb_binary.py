#!/usr/bin/env python3
"""
Generate a synthetic RG10 (10-bit) RGGB Bayer pattern image as a binary file or send to camera.
Usage: python generate_rg10_rggb_binary.py <R> <G> <B> <width> <height> <output_file> <mode>
  <mode>: "binary" to write file, "camera" to send to camera (mock)
"""
import sys
import struct

USAGE = (
    "Usage: python generate_rg10_rggb_binary.py <R> <G> <B> <width> <height> binary <output_file>\n"
    "   or: python generate_rg10_rggb_binary.py <R> <G> <B> camera"
)


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

def mock_send_to_camera(data):
    print(f"[MOCK] Sending RGB values {data[:6].hex()} to camera")


def main():
    if len(sys.argv) < 5:  # Need at least R,G,B and mode
        print(USAGE)
        sys.exit(1)

    try:
        R = validate_color(sys.argv[1], 'R')
        G = validate_color(sys.argv[2], 'G')
        B = validate_color(sys.argv[3], 'B')

        # Check the mode first
        if len(sys.argv) >= 7 and sys.argv[6].lower() == "binary":
            MODE = "binary"
            WIDTH = int(sys.argv[4])
            HEIGHT = int(sys.argv[5])
            if len(sys.argv) != 8:
                print(USAGE)
                sys.exit(1)
            outfile = sys.argv[7]
        elif len(sys.argv) == 5 and sys.argv[4].lower() == "camera":
            MODE = "camera"
            WIDTH = HEIGHT = None  # Camera will determine size
            outfile = None
        else:
            print(USAGE)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        print(USAGE)
        sys.exit(1)

    # Generate image data
    image_data = bytearray()
    if MODE == "binary":
        for y in range(HEIGHT):
            for x in range(WIDTH):
                # RGGB Bayer pattern
                if y % 2 == 0:
                    color = R if x % 2 == 0 else G
                else:
                    color = G if x % 2 == 0 else B
                image_data.extend(to_rg10_bytes(color))

    if MODE == "binary":
        with open(outfile, 'wb') as f:
            f.write(image_data)
        print(f"RG10 RGGB binary image written to {outfile}")
    elif MODE == "camera":
        # For camera mode, just send the RGB values
        camera_data = bytearray()
        camera_data.extend(to_rg10_bytes(R))
        camera_data.extend(to_rg10_bytes(G))
        camera_data.extend(to_rg10_bytes(B))
        mock_send_to_camera(camera_data)


if __name__ == "__main__":
    main()
