#!/usr/bin/env python3
"""
Send RGB values to camera via I2C in RG10 format.
Usage: python send_rg10_to_camera.py <R> <G> <B>
"""
import sys
import subprocess
from smbus2 import SMBus

I2C_BUS = 2
I2C_ADDR = 0x10
REG_R_LSB_ADDR = 0x602
REG_G1_LSB_ADDR = 0x604
REG_G2_LSB_ADDR = 0x606
REG_B_LSB_ADDR = 0x608

USAGE = "Usage: python send_rg10_to_camera.py <R> <G> <B>"


def validate_color(val, name):
    if not val.isdigit():
        raise ValueError(f"{name} value must be an integer.")
    ival = int(val)
    if not (0 <= ival <= 1023):
        raise ValueError(f"{name} value must be between 0 and 1023.")
    return ival


def convert_10bit_to_16bit(value):
    """Convert a 10-bit value into LSB (8 bits) and MSB (2 bits) bytes."""
    if not (0 <= value <= 1023):
        raise ValueError("Value out of 10-bit range")
    lsb = value & 0xFF         # Lower 8 bits
    msb = (value >> 8) & 0x03  # Upper 2 bits

    return lsb, msb

def log_register_write(value, reg_lsb_addr, lsb, msb):
    """Log the register write operation."""
    print(f"Converting value 0x{value:03x} -> reg 0x{reg_lsb_addr:03x}[7:0]=0x{lsb:02x}, reg 0x{reg_lsb_addr+1:03x}[1:0]=0x{msb:02x}")

def write_i2c(bus, lsb, msb, reg_lsb_addr):
    """Write LSB and MSB bytes to two consecutive I2C registers."""
    try:
        bus.write_byte_data(I2C_ADDR, reg_lsb_addr, lsb)
        bus.write_byte_data(I2C_ADDR, reg_lsb_addr + 1, msb)
    except Exception as e:
        print(f"Failed to write to I2C: {e}")


def send_to_camera(r_bytes, g1_bytes, g2_bytes, b_bytes):
    """Send pre-converted RGB values to camera via I2C."""
    print(f"Attempting to write values to camera via I2C:")
    try:
        with SMBus(I2C_BUS) as bus:
            write_i2c(bus, r_bytes[0], r_bytes[1], REG_R_LSB_ADDR)
            write_i2c(bus, g1_bytes[0], g1_bytes[1], REG_G1_LSB_ADDR)
            write_i2c(bus, g2_bytes[0], g2_bytes[1], REG_G2_LSB_ADDR)
            write_i2c(bus, b_bytes[0], b_bytes[1], REG_B_LSB_ADDR)
        print("Complete: RGB values written to camera registers")
    except Exception as e:
        print(f"Failed to write to I2C: {e}")

def setup():
    print(f"Setting up")
    # Any additional setup can be done here if needed
    cmd = [sys.executable, "rmmod" , "li_imx477"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        sys.exit(1)

def clear():
    print(f"Clearing")
    # Any additional cleanup can be done here if needed
    cmd = [sys.executable, "modprobe" , "li_imx477"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        sys.exit(1)

    cmd = [sys.executable, "systemctl" , "restart", "nvargus-daemon"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        sys.exit(1)

def show():
    cmd = [sys.executable, "gst-launch-1.0" , "nvaguscamerasrc", "sensor-id=1", "sensor-mode=0", "!", "nv3dsink"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        print(USAGE)
        sys.exit(1)

    try:
        r = validate_color(sys.argv[1], 'R')
        g = validate_color(sys.argv[2], 'G')
        b = validate_color(sys.argv[3], 'B')
    except Exception as e:
        print(f"Error: {e}")
        print(USAGE)
        sys.exit(1)

    # Convert and log all values before attempting any I2C operations
    r_lsb, r_msb = convert_10bit_to_16bit(r)
    g_lsb, g_msb = convert_10bit_to_16bit(g)
    b_lsb, b_msb = convert_10bit_to_16bit(b)

    # Log all register writes
    log_register_write(r, REG_R_LSB_ADDR, r_lsb, r_msb)
    log_register_write(g, REG_G1_LSB_ADDR, g_lsb, g_msb)
    log_register_write(g, REG_G2_LSB_ADDR, g_lsb, g_msb)
    log_register_write(b, REG_B_LSB_ADDR, b_lsb, b_msb)

    try:
        setup()

        print(f"Preparing values for I2C bus {I2C_BUS}, device address 0x{I2C_ADDR:02x}:")
        # Pass pre-converted bytes to send_to_camera
        send_to_camera(
            (r_lsb, r_msb),
            (g_lsb, g_msb),
            (g_lsb, g_msb),
            (b_lsb, b_msb)
        )

        clear()
        show()
    except Exception as e:
        print(f"Error communicating with camera via I2C: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
