# 🔐 PIN Generator

A secure PIN generator written in Python. Filters out common patterns, repeated digits, and predictable combinations. Can also score the strength of an existing PIN.

## Features

- Generate PINs with **4, 6, or 8 digits**
- Filters weak patterns (1234, 0000, 8999, AABB, etc.)
- **Strength checker** for your existing PIN (score 1–10)
- Uses `secrets` module — cryptographically secure random generator

## Requirements

Python 3.8+ — no external dependencies.

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/pin-generator.git
cd pin-generator
python pin_gen.py
```

## Usage

### Generate a PIN

```bash
# 5 PINs, 4 digits (default)
python pin_gen.py

# 6-digit PINs
python pin_gen.py generate --length 6

# 8-digit PINs, 3 options
python pin_gen.py generate --length 8 --count 3

# Short form
python pin_gen.py g -l 6 -n 3
```

### Check your own PIN

```bash
python pin_gen.py check 8472
python pin_gen.py c 382917
```

## Example output

```
🔐 Secure 4-digit PINs:

  1. 3891
  2. 6824
  3. 7329
  4. 0647
  5. 5183

🔍 PIN check: ****
   🟢 Strong  (8/10)
```

## What counts as a weak PIN

| Pattern | Example |
|---|---|
| All digits the same | `0000`, `1111` |
| Sequence | `1234`, `4321`, `2468` |
| Common combinations | `2580`, `6969`, `1337` |
| Looks like a year | `1998`, `200134` |
| Three identical in a row | `8999`, `1222` |
| AABB pattern | `1122`, `3344` |

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE) for details.

Any derivative work **must remain open source** under the same license.
