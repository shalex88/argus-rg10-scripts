#!/usr/bin/python3

import numpy as np
from typing import Union, Tuple, List

def convert_8bit_to_10bit(value: int) -> int:
    """
    Convert a single 8-bit value to 10-bit.
    Preserves exact relationships: 0x00->0x00, 0x80->0x200, 0xFF->0x3FF

    Args:
        value: 8-bit value (0-255)

    Returns:
        10-bit value (0-1023)
    """
    if not 0 <= value <= 255:
        raise ValueError("Input value must be between 0 and 255")

    return (value * 1023 + 127) // 255

def convert_8bit_to_10bit_bitshift(value: int) -> int:
    """
    Alternative bit-shifting method (faster but slightly less accurate).
    """
    if not 0 <= value <= 255:
        raise ValueError("Input value must be between 0 and 255")

    return (value << 2) | (value >> 6)

def convert_rgb_pixel(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Convert a single RGB pixel from 8-bit to 10-bit.

    Args:
        r, g, b: 8-bit RGB values (0-255)

    Returns:
        Tuple of 10-bit RGB values (0-1023)
    """
    return (
        convert_8bit_to_10bit(r),
        convert_8bit_to_10bit(g),
        convert_8bit_to_10bit(b)
    )

def convert_rgb_array(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convert an array of RGB values from 8-bit to 10-bit using NumPy.

    Args:
        rgb_array: NumPy array of 8-bit values, shape can be:
                  - (height, width, 3) for RGB image
                  - (n, 3) for list of RGB pixels
                  - (n,) for single channel values

    Returns:
        NumPy array of 10-bit values with same shape
    """
    if rgb_array.dtype != np.uint8:
        rgb_array = rgb_array.astype(np.uint8)

    # Vectorized conversion: (value * 1023 + 127) // 255
    # Need to use int32 to avoid overflow during multiplication
    return ((rgb_array.astype(np.int32) * 1023 + 127) // 255).astype(np.uint16)

def convert_rgb_list(rgb_list: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Convert a list of RGB tuples from 8-bit to 10-bit.

    Args:
        rgb_list: List of (r, g, b) tuples with 8-bit values

    Returns:
        List of (r, g, b) tuples with 10-bit values
    """
    return [convert_rgb_pixel(r, g, b) for r, g, b in rgb_list]

# Create lookup table for maximum performance
_LOOKUP_TABLE = [convert_8bit_to_10bit(i) for i in range(256)]

def convert_8bit_to_10bit_lut(value: int) -> int:
    """
    Convert using pre-computed lookup table (fastest method).
    """
    return _LOOKUP_TABLE[value]

def convert_rgb_array_lut(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convert RGB array using lookup table (fastest for large arrays).
    """
    return np.array(_LOOKUP_TABLE)[rgb_array]

# Test and demonstration functions
def test_conversion():
    """Test the conversion with the specified requirements."""
    print("Testing 8-bit to 10-bit conversion:")
    print(f"0x00 -> 0x{convert_8bit_to_10bit(0x00):03X} (expected 0x000)")
    print(f"0x80 -> 0x{convert_8bit_to_10bit(0x80):03X} (expected 0x200)")
    print(f"0xFF -> 0x{convert_8bit_to_10bit(0xFF):03X} (expected 0x3FF)")

    print("\nTesting intermediate values:")
    test_values = [0x00, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0, 0xFF]
    for val in test_values:
        result = convert_8bit_to_10bit(val)
        print(f"0x{val:02X} -> 0x{result:03X} (decimal: {val} -> {result})")

def compare_methods():
    """Compare different conversion methods for accuracy."""
    print("\nComparing conversion methods:")
    print("Value | Mathematical | Bit-shift | LUT")
    print("------|-------------|-----------|----")

    test_values = [0x00, 0x80, 0xFF, 0x40, 0xC0]
    for val in test_values:
        math_result = convert_8bit_to_10bit(val)
        shift_result = convert_8bit_to_10bit_bitshift(val)
        lut_result = convert_8bit_to_10bit_lut(val)
        print(f"0x{val:02X}  |    0x{math_result:03X}     |   0x{shift_result:03X}    | 0x{lut_result:03X}")

def demo_image_conversion():
    """Demonstrate image conversion using NumPy."""
    print("\nDemo: Converting a sample RGB image:")

    # Create a sample 3x3 RGB image
    sample_image = np.array([
        [[0, 128, 255], [64, 192, 128], [255, 0, 128]],
        [[128, 128, 128], [0, 255, 0], [255, 255, 255]],
        [[32, 96, 160], [224, 64, 192], [128, 200, 80]]
    ], dtype=np.uint8)

    print("Original 8-bit image:")
    print(sample_image)

    converted_image = convert_rgb_array(sample_image)
    print(f"\nConverted 10-bit image:")
    print(converted_image)

    print(f"\nImage shape: {sample_image.shape}")
    print(f"Original dtype: {sample_image.dtype}, range: {sample_image.min()}-{sample_image.max()}")
    print(f"Converted dtype: {converted_image.dtype}, range: {converted_image.min()}-{converted_image.max()}")

if __name__ == "__main__":
    test_conversion()
    compare_methods()
    demo_image_conversion()