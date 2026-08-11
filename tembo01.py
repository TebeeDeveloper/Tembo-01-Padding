def tembo01_pad(data: bytes, block_size: int = 8) -> bytes:
    """
    Applies Tembo#01 padding scheme.

    Designed to fix two weaknesses in ISO/IEC 7816-4 padding:
      1. Uses 0xBF instead of 0x00 for intermediate bytes → harder to guess.
      2. Always adds padding, even when data length is already a multiple of block size → prevents length-based attacks.

    Args:
        data: Original data as bytes.
        block_size: Target block size in bytes (default: 8).

    Returns:
        Data with padding appended.
    """
    data_length = len(data)
    pad_length = block_size - (data_length % block_size)
    if pad_length < 2:
        pad_length += block_size# ALWAYS compute, even if aligned
        # Format: [0x80][0xBF ...][pad_length]
        padding = b"\x80" + b"\xBF" * (pad_length - 2) + bytes([pad_length])

    return data + padding


def tembo01_unpad(padded_data: bytes) -> bytes:
    """
    Removes Tembo#01 padding and returns original data.

    Args:
        padded_data: Data with Tembo#01 padding applied.

    Returns:
        Original data without padding.
    """
    pad_length = padded_data[-1]  # Last byte = padding length
    return padded_data[:-pad_length]


# ==================== TEST CASES ====================
if __name__ == "__main__":
    print("=== TEMBO#01 — TEST SUITE ===\n")

    # Case 1: Data shorter than block size
    d1 = b"ABCDE"        # 5 bytes, block 8 → pad 3 bytes
    p1 = tembo01_pad(d1, 8)
    assert tembo01_unpad(p1) == d1
    print(f"[1] 5 bytes → padded: {p1.hex(' ')}")
    print(f"    Round-trip OK: {tembo01_unpad(p1) == d1}\n")

    # Case 2: Data EXACTLY aligned → STILL ADD PAD ⭐ key difference
    d2 = b"ABCDEFGH"     # exactly 8 bytes
    p2 = tembo01_pad(d2, 8)
    assert tembo01_unpad(p2) == d2
    print(f"[2] 8 bytes (aligned) → padded: {p2.hex(' ')}")
    print(f"    Round-trip OK: {tembo01_unpad(p2) == d2}\n")

    # Case 3: Missing exactly 1 byte → pad_length = 1
    d3 = b"ABCDEFG"      # 7 bytes
    p3 = tembo01_pad(d3, 8)
    assert tembo01_unpad(p3) == d3
    print(f"[3] 7 bytes → padded: {p3.hex(' ')}")
    print(f"    Round-trip OK: {tembo01_unpad(p3) == d3}\n")

    # Case 4: 16-byte block size
    d4 = b"Hello Tembo"  # 12 bytes
    p4 = tembo01_pad(d4, 16)
    assert tembo01_unpad(p4) == d4
    print(f"[4] 12 bytes / block 16 → padded: {p4.hex(' ')}")
    print(f"    Round-trip OK: {tembo01_unpad(p4) == d4}\n")

    print("✅ ALL TESTS PASSED! Tembo#01 works correctly!")
