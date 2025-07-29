#!/usr/bin/python3

import numpy as np
from typing import Union, Tuple, List

def convert_8bit_to_10bit_16bit(value: int) -> int:
    """
    Convert a single 8-bit value to 10-bit, returned as 16-bit register format.
    Preserves exact relationships: 0x00->0x0000, 0x80->0x0200, 0xFF->0x03FF
    Upper 6 bits are zero (typical hardware register format).

    Args:
        value: 8-bit value (0-255)

    Returns:
        16-bit register value with 10-bit data in lower bits (0x0000-0x03FF)
    """
    if not 0 <= value <= 255:
        raise ValueError("Input value must be between 0 and 255")

    # Convert to 10-bit and ensure it fits in 16-bit register
    result_10bit = (value * 1023 + 127) // 255
    return result_10bit & 0x03FF  # Mask to ensure 10-bit result in 16-bit register

def convert_8bit_to_10bit_scaled_16bit(value: int) -> int:
    """
    Convert a single 8-bit value to 10-bit, then multiply by 16 (scale by 16).
    Preserves exact relationships: 0x00->0x0000, 0x80->0x2000, 0xFF->0x3FF0
    Result uses upper 14 bits of 16-bit register.

    Args:
        value: 8-bit value (0-255)

    Returns:
        16-bit register value with scaled 10-bit data (0x0000-0x3FF0, multiples of 16)
    """
    if not 0 <= value <= 255:
        raise ValueError("Input value must be between 0 and 255")

    # Convert to 10-bit first
    result_10bit = (value * 1023 + 127) // 255
    # Scale by 16 (left shift by 4 bits) and ensure it fits in 16-bit
    result_scaled = (result_10bit << 4) & 0xFFFF
    return result_scaled

def convert_8bit_to_10bit_bitshift_16bit(value: int) -> int:
    """
    Alternative bit-shifting method (faster but slightly less accurate).
    Returns 16-bit register format.
    """
    if not 0 <= value <= 255:
        raise ValueError("Input value must be between 0 and 255")

    result = (value << 2) | (value >> 6)
    return result & 0x03FF  # Ensure 16-bit register format

def convert_8bit_to_10bit_bitshift_scaled_16bit(value: int) -> int:
    """
    Alternative bit-shifting method with 16x scaling.
    Returns scaled 16-bit register format.
    """
    if not 0 <= value <= 255:
        raise ValueError("Input value must be between 0 and 255")

    result = (value << 2) | (value >> 6)
    result_scaled = (result << 4) & 0xFFFF  # Scale by 16 and mask to 16-bit
    return result_scaled

def convert_rgb_pixel_16bit(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Convert a single RGB pixel from 8-bit to 10-bit in 16-bit register format.

    Args:
        r, g, b: 8-bit RGB values (0-255)

    Returns:
        Tuple of 16-bit register values containing 10-bit RGB data (0x0000-0x03FF each)
    """
    return (
        convert_8bit_to_10bit_16bit(r),
        convert_8bit_to_10bit_16bit(g),
        convert_8bit_to_10bit_16bit(b)
    )

def convert_rgb_pixel_scaled_16bit(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Convert a single RGB pixel from 8-bit to 10-bit with 16x scaling in 16-bit register format.

    Args:
        r, g, b: 8-bit RGB values (0-255)

    Returns:
        Tuple of 16-bit register values containing scaled 10-bit RGB data (0x0000-0x3FF0 each)
    """
    return (
        convert_8bit_to_10bit_scaled_16bit(r),
        convert_8bit_to_10bit_scaled_16bit(g),
        convert_8bit_to_10bit_scaled_16bit(b)
    )

def convert_rgb_array_16bit(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convert an array of RGB values from 8-bit to 10-bit using NumPy.
    Results stored in 16-bit register format.

    Args:
        rgb_array: NumPy array of 8-bit values, shape can be:
                  - (height, width, 3) for RGB image
                  - (n, 3) for list of RGB pixels
                  - (n,) for single channel values

    Returns:
        NumPy array of uint16 values with 10-bit data in lower bits
    """
    if rgb_array.dtype != np.uint8:
        rgb_array = rgb_array.astype(np.uint8)

    # Vectorized conversion: (value * 1023 + 127) // 255
    # Use int32 to avoid overflow, then convert to uint16
    result = ((rgb_array.astype(np.int32) * 1023 + 127) // 255)

    # Ensure 10-bit values in 16-bit registers and convert to uint16
    return (result & 0x03FF).astype(np.uint16)

def convert_rgb_array_scaled_16bit(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convert an array of RGB values from 8-bit to 10-bit with 16x scaling using NumPy.
    Results stored in 16-bit register format.

    Args:
        rgb_array: NumPy array of 8-bit values, shape can be:
                  - (height, width, 3) for RGB image
                  - (n, 3) for list of RGB pixels
                  - (n,) for single channel values

    Returns:
        NumPy array of uint16 values with scaled 10-bit data
    """
    if rgb_array.dtype != np.uint8:
        rgb_array = rgb_array.astype(np.uint8)

    # Vectorized conversion: (value * 1023 + 127) // 255
    # Use int32 to avoid overflow
    result = ((rgb_array.astype(np.int32) * 1023 + 127) // 255)
    
    # Scale by 16 (left shift by 4 bits) and ensure it fits in 16-bit
    result_scaled = (result << 4) & 0xFFFF
    
    return result_scaled.astype(np.uint16)

def convert_rgb_list_16bit(rgb_list: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Convert a list of RGB tuples from 8-bit to 10-bit in 16-bit register format.

    Args:
        rgb_list: List of (r, g, b) tuples with 8-bit values

    Returns:
        List of (r, g, b) tuples with 16-bit register values containing 10-bit data
    """
    return [convert_rgb_pixel_16bit(r, g, b) for r, g, b in rgb_list]

def convert_rgb_list_scaled_16bit(rgb_list: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Convert a list of RGB tuples from 8-bit to 10-bit with 16x scaling in 16-bit register format.

    Args:
        rgb_list: List of (r, g, b) tuples with 8-bit values

    Returns:
        List of (r, g, b) tuples with 16-bit register values containing scaled 10-bit data
    """
    return [convert_rgb_pixel_scaled_16bit(r, g, b) for r, g, b in rgb_list]

# Create lookup tables for maximum performance
_LOOKUP_TABLE_16BIT = [convert_8bit_to_10bit_16bit(i) for i in range(256)]
_LOOKUP_TABLE_SCALED_16BIT = [convert_8bit_to_10bit_scaled_16bit(i) for i in range(256)]

def convert_8bit_to_10bit_lut_16bit(value: int) -> int:
    """
    Convert using pre-computed lookup table (fastest method).
    Returns 16-bit register format.
    """
    return _LOOKUP_TABLE_16BIT[value]

def convert_8bit_to_10bit_lut_scaled_16bit(value: int) -> int:
    """
    Convert using pre-computed lookup table with 16x scaling (fastest method).
    Returns scaled 16-bit register format.
    """
    return _LOOKUP_TABLE_SCALED_16BIT[value]

def convert_rgb_array_lut_16bit(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convert RGB array using lookup table (fastest for large arrays).
    Returns 16-bit register format.
    """
    return np.array(_LOOKUP_TABLE_16BIT, dtype=np.uint16)[rgb_array]

def convert_rgb_array_lut_scaled_16bit(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convert RGB array using lookup table with 16x scaling (fastest for large arrays).
    Returns scaled 16-bit register format.
    """
    return np.array(_LOOKUP_TABLE_SCALED_16BIT, dtype=np.uint16)[rgb_array]

# Hardware register analysis functions
def analyze_register_format(value_10bit: int, scaled: bool = False) -> dict:
    """
    Analyze the 16-bit register format for a 10-bit value.

    Args:
        value_10bit: 10-bit value (0-1023) or scaled value if scaled=True
        scaled: Whether the value is already scaled by 16

    Returns:
        Dictionary with bit field analysis
    """
    if scaled:
        if not 0 <= value_10bit <= 0x3FF0:
            raise ValueError("Input must be a valid scaled 10-bit value (0-0x3FF0)")
        reg_16bit = value_10bit & 0xFFFF
        actual_10bit = value_10bit >> 4
    else:
        if not 0 <= value_10bit <= 1023:
            raise ValueError("Input must be a valid 10-bit value (0-1023)")
        reg_16bit = value_10bit & 0x03FF
        actual_10bit = value_10bit

    return {
        'value_10bit': actual_10bit,
        'register_16bit': reg_16bit,
        'hex_representation': f"0x{reg_16bit:04X}",
        'binary_representation': f"0b{reg_16bit:016b}",
        'used_bits': f"bits [13:4] = 0b{actual_10bit:010b}" if scaled else f"bits [9:0] = 0b{reg_16bit:010b}",
        'unused_bits': f"bits [15:14,3:0] = 0b{(reg_16bit >> 14):02b}{'0000' if scaled else f'{(reg_16bit >> 10):06b}'}" + (" (should be 00,0000)" if scaled else " (should be 000000)"),
        'bit_utilization': f"{10 if not scaled else 10}/16 bits used ({(10 if not scaled else 10)/16*100:.1f}%)",
        'scaling_factor': 16 if scaled else 1
    }

def display_register_map(rgb_values_8bit: Tuple[int, int, int], scaled: bool = False) -> None:
    """
    Display detailed register mapping for RGB conversion.

    Args:
        rgb_values_8bit: Tuple of (r, g, b) 8-bit values
        scaled: Whether to show scaled (16x) version
    """
    r8, g8, b8 = rgb_values_8bit
    
    if scaled:
        r16, g16, b16 = convert_rgb_pixel_scaled_16bit(r8, g8, b8)
        print(f"\n=== RGB Register Mapping (16x Scaled) ===")
    else:
        r16, g16, b16 = convert_rgb_pixel_16bit(r8, g8, b8)
        print(f"\n=== RGB Register Mapping ===")
    
    print(f"Input 8-bit RGB: ({r8}, {g8}, {b8}) = (0x{r8:02X}, 0x{g8:02X}, 0x{b8:02X})")
    print(f"Output 16-bit registers: ({r16}, {g16}, {b16}) = (0x{r16:04X}, 0x{g16:04X}, 0x{b16:04X})")

    print(f"\nRegister Details:")
    for val8, val16, name in [(r8, r16, 'Red'), (g8, g16, 'Green'), (b8, b16, 'Blue')]:
        analysis = analyze_register_format(val16, scaled=scaled)
        print(f"\n{name} Channel:")
        print(f"  8-bit input:  0x{val8:02X} ({val8:3d})")
        print(f"  16-bit reg:   {analysis['hex_representation']} ({val16:4d})")
        print(f"  Binary:       {analysis['binary_representation']}")
        print(f"  Data bits:    {analysis['used_bits']}")
        print(f"  Unused bits:  {analysis['unused_bits']}")
        if scaled:
            print(f"  10-bit value: {analysis['value_10bit']} (before 16x scaling)")

# Test and demonstration functions
def test_conversion_16bit():
    """Test the conversion with 16-bit register format."""
    print("Testing 8-bit to 10-bit conversion (16-bit register format):")
    print(f"0x00 -> 0x{convert_8bit_to_10bit_16bit(0x00):04X} (expected 0x0000)")
    print(f"0x80 -> 0x{convert_8bit_to_10bit_16bit(0x80):04X} (expected 0x0200)")
    print(f"0xFF -> 0x{convert_8bit_to_10bit_16bit(0xFF):04X} (expected 0x03FF)")

    print(f"\nTesting 8-bit to 10-bit conversion with 16x scaling:")
    print(f"0x00 -> 0x{convert_8bit_to_10bit_scaled_16bit(0x00):04X} (expected 0x0000)")
    print(f"0x80 -> 0x{convert_8bit_to_10bit_scaled_16bit(0x80):04X} (expected 0x2000)")
    print(f"0xFF -> 0x{convert_8bit_to_10bit_scaled_16bit(0xFF):04X} (expected 0x3FF0)")

    print(f"\nMaximum values check:")
    print(f"10-bit max: 0x{1023:04X} (0x03FF)")
    print(f"Scaled max: 0x{1023*16:04X} (0x3FF0)")
    print(f"Register bit mask (unscaled): 0x{0x03FF:04X}")
    print(f"Register bit mask (scaled): 0x{0xFFFF:04X}")

    print("\nTesting intermediate values:")
    test_values = [0x00, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0, 0xFF]
    print("Value | Unscaled | Scaled")
    print("------|----------|--------")
    for val in test_values:
        result = convert_8bit_to_10bit_16bit(val)
        result_scaled = convert_8bit_to_10bit_scaled_16bit(val)
        print(f"0x{val:02X}  |  0x{result:04X}   | 0x{result_scaled:04X}")

def compare_methods_16bit():
    """Compare different conversion methods for accuracy (16-bit format)."""
    print("\nComparing conversion methods (16-bit register format):")
    print("Value | Math  | Shift | LUT   | Math*16 | Shift*16 | LUT*16")
    print("------|-------|-------|-------|---------|----------|--------")

    test_values = [0x00, 0x80, 0xFF, 0x40, 0xC0]
    for val in test_values:
        math_result = convert_8bit_to_10bit_16bit(val)
        shift_result = convert_8bit_to_10bit_bitshift_16bit(val)
        lut_result = convert_8bit_to_10bit_lut_16bit(val)
        math_scaled = convert_8bit_to_10bit_scaled_16bit(val)
        shift_scaled = convert_8bit_to_10bit_bitshift_scaled_16bit(val)
        lut_scaled = convert_8bit_to_10bit_lut_scaled_16bit(val)
        print(f"0x{val:02X}  | 0x{math_result:04X} | 0x{shift_result:04X} | 0x{lut_result:04X} |  0x{math_scaled:04X}  |  0x{shift_scaled:04X}   | 0x{lut_scaled:04X}")

def demo_image_conversion_16bit():
    """Demonstrate image conversion using NumPy with 16-bit register format."""
    print("\nDemo: Converting a sample RGB image (16-bit register format):")

    # Create a sample 3x3 RGB image
    sample_image = np.array([
        [[0, 128, 255], [64, 192, 128], [255, 0, 128]],
        [[128, 128, 128], [0, 255, 0], [255, 255, 255]],
        [[32, 96, 160], [224, 64, 192], [128, 200, 80]]
    ], dtype=np.uint8)

    print("Original 8-bit image:")
    print(sample_image)

    converted_image = convert_rgb_array_16bit(sample_image)
    converted_image_scaled = convert_rgb_array_scaled_16bit(sample_image)
    
    print(f"\nConverted 10-bit image (in 16-bit registers):")
    print(converted_image)
    
    print(f"\nConverted 10-bit image with 16x scaling (in 16-bit registers):")
    print(converted_image_scaled)

    # Show hexadecimal representation
    print(f"\nConverted image (hexadecimal, unscaled):")
    for i in range(converted_image.shape[0]):
        row_hex = []
        for j in range(converted_image.shape[1]):
            pixel_hex = [f"0x{val:04X}" for val in converted_image[i, j]]
            row_hex.append(f"[{', '.join(pixel_hex)}]")
        print(f"  {', '.join(row_hex)}")
    
    print(f"\nConverted image (hexadecimal, 16x scaled):")
    for i in range(converted_image_scaled.shape[0]):
        row_hex = []
        for j in range(converted_image_scaled.shape[1]):
            pixel_hex = [f"0x{val:04X}" for val in converted_image_scaled[i, j]]
            row_hex.append(f"[{', '.join(pixel_hex)}]")
        print(f"  {', '.join(row_hex)}")

    print(f"\nImage shape: {sample_image.shape}")
    print(f"Original dtype: {sample_image.dtype}, range: {sample_image.min()}-{sample_image.max()}")
    print(f"Converted dtype: {converted_image.dtype}, range: {converted_image.min()}-{converted_image.max()}")
    print(f"Scaled dtype: {converted_image_scaled.dtype}, range: {converted_image_scaled.min()}-{converted_image_scaled.max()}")
    print(f"Register format (unscaled): 16-bit with 10-bit data (max value: 0x{converted_image.max():04X})")
    print(f"Register format (scaled): 16-bit with scaled 10-bit data (max value: 0x{converted_image_scaled.max():04X})")

def demo_register_analysis():
    """Demonstrate register format analysis."""
    print("\n=== Register Format Analysis Demo ===")

    # Test with some sample RGB values
    test_pixels = [
        (0, 0, 0),        # Black
        (128, 128, 128),  # Gray
        (255, 255, 255),  # White
        (255, 0, 0),      # Red
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
    ]

    for rgb in test_pixels:
        display_register_map(rgb, scaled=False)
        display_register_map(rgb, scaled=True)

if __name__ == "__main__":
    test_conversion_16bit()
    compare_methods_16bit()
    #demo_image_conversion_16bit()
    #demo_register_analysis()
