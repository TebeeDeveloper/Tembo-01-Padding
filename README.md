# 🛡️ Tembo#01 Padding Scheme

> A secure padding scheme designed to fix two critical weaknesses in ISO/IEC 7816-4 padding.
> Created by a 15-year-old developer — Released under the **GNU GPL v3.0**.

---

## 🎯 What Problem Does It Solve?

ISO/IEC 7816-4 padding has two well-known flaws:

1. **Predictable padding bytes**: Uses `0x80` followed by all `0x00` → easy to guess and analyze statistically.
2. **No padding when data is block-aligned**: If data length already matches a multiple of block size → **no padding is added** → leaks information via message length → vulnerable to **length-based attacks**.

✅ **Tembo#01 fixes BOTH issues.**

---

## ✨ Key Features

- 🛡️ **Harder to guess**: Uses `0xBF` instead of `0x00` for intermediate padding bytes
- 🛡️ **Always pads**: Padding is ALWAYS appended, even when data is perfectly aligned → blocks length-based attacks
- 🛡️ **Self-describing length**: Last byte = padding length → unambiguous removal
- 🛡️ **Simple & lightweight**: Only basic byte operations, no dependencies
- 🆓 **Free & Open Source**: Licensed under **GNU GPL v3.0** — forever open!

---

## 📐 Specification

### Padding Rules
1. **Calculate padding length:** pad_len = block_size − (data_length % block_size)
If `data_length % block_size == 0`, then `pad_len = block_size` — **ALWAYS add padding!**

2. **Padding byte sequence:**
`[0x80] + [0xBF × (pad_len − 2)] + [pad_len]`

3. **Unpadding:** Read the **last byte** → that is `pad_len` → remove last `pad_len` bytes.

---

## Python Implementation

```python
# SPDX-License-Identifier: GPL-3.0-or-later

def tembo01_pad(data: bytes, block_size: int = 8) -> bytes:
    """Apply Tembo#01 padding."""
    data_length = len(data)
    pad_length = block_size - (data_length % block_size)
    if pad_length < 2:
        pad_length += block_size
    padding = b"\x80" + b"\xBF" * (pad_length - 2) + bytes([pad_length])
    return data + padding


def tembo01_unpad(padded_data: bytes) -> bytes:
    """Remove Tembo#01 padding."""
    pad_length = padded_data[-1]
    id padded_data[-pad_length] != 0x80:
        raise Exception("Padding byte error!")
        return b""
    return padded_data[:-pad_length]
```

---

## Quick Example
```python
# Example 1: Data shorter than block
data = b"ABCDE"          # 5 bytes
padded = tembo01_pad(data, 8)
print(padded.hex(" "))    # 41 42 43 44 45 80 bf 03
original = tembo01_unpad(padded)

# Example 2: Perfectly aligned — STILL PADDED! ⭐
data = b"ABCDEFGH"       # 8 bytes
padded = tembo01_pad(data, 8)
# Result: 8 bytes of padding added! Length no longer leaks info!
```

---

## Comparison vs ISO/IEC 7816-4
Aspect | ISO/IEC 7816-4 | Tembo#01
|---|---|---|
Intermediate bytes | 0x00 — very predictable ✗ | 0xBF — harder to guess ✅
Aligned data | No padding → vulnerable ✗ | Always pad → protected ✅
Padding length | Ambiguous | Last byte = length → clear ✅
Security level |	Basic |	Improved ✅

---

## License
**Tembo#01 — Secure Padding Scheme**

Copyright © 2026 Created by a 15-year-old developer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3.0 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License v3.0
along with this program. If not, see https://www.gnu.org/licenses/.
