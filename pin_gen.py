# PIN Generator — secure PIN generator
# Copyright (C) 2026  nzteam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import secrets
import argparse

# ── Blacklist ──────────────────────────────────────────────────────────────
BAD_PINS_4 = {
    "1234","0000","1111","2222","3333","4444","5555","6666","7777","8888",
    "9999","1212","2580","0852","4321","1122","1313","0001","1000","1010",
    "2000","2001","1999","2004","6969","4200","1337","0420","1004",
    "2468","1357","9876","1230","0123",
}
BAD_PINS_6 = {
    "123456","000000","111111","123123","321321","112233",
    "696969","654321","159753","147258",
}
BAD_PINS_8 = {
    "12345678","00000000","11111111","87654321","12341234",
}

BAD_MAP = {4: BAD_PINS_4, 6: BAD_PINS_6, 8: BAD_PINS_8}
YEAR_PREFIXES = {4: ("19","20"), 6: ("199","200","198"), 8: ("1990","1985","2000","2001")}

# ── Checks ─────────────────────────────────────────────────────────────────
def is_weak(pin: str) -> tuple[bool, str]:
    length = len(pin)
    digits = [int(d) for d in pin]

    if len(set(digits)) == 1:
        return True, "all digits are the same"

    diffs = [digits[i+1] - digits[i] for i in range(length - 1)]
    if all(d == diffs[0] for d in diffs):
        return True, "digits form a sequence"

    if pin in BAD_MAP.get(length, set()):
        return True, "too common"

    for prefix in YEAR_PREFIXES.get(length, ()):
        if pin.startswith(prefix):
            return True, "looks like a year"

    if len(set(digits)) < max(2, length // 2):
        return True, "too few unique digits"

    if any(digits[i] == digits[i+1] == digits[i+2] for i in range(length - 2)):
        return True, "three identical digits in a row"

    if length >= 4 and digits[0] == digits[1] and digits[2] == digits[3]:
        return True, "AABB pattern"

    return False, ""

# ── Generator ──────────────────────────────────────────────────────────────
def generate_pin(length: int = 4) -> str:
    if length not in (4, 6, 8):
        raise ValueError("PIN length must be 4, 6, or 8")
    while True:
        pin = "".join(str(secrets.randbelow(10)) for _ in range(length))
        weak, _ = is_weak(pin)
        if not weak:
            return pin

# ── Scorer ─────────────────────────────────────────────────────────────────
def score_pin(pin: str) -> dict:
    if not pin.isdigit():
        return {"score": 0, "label": "❌ Error", "reason": "PIN must contain digits only"}

    length = len(pin)
    if length not in (4, 6, 8):
        return {"score": 0, "label": "❌ Error", "reason": "Length must be 4, 6, or 8 digits"}

    weak, reason = is_weak(pin)
    if weak:
        return {"score": 1, "label": "🔴 Very weak", "reason": reason}

    digits = [int(d) for d in pin]
    score = 5

    unique_ratio = len(set(digits)) / length
    if unique_ratio >= 0.75:
        score += 2
    elif unique_ratio >= 0.5:
        score += 1

    if length == 6:
        score += 1
    elif length == 8:
        score += 3

    pairs = sum(1 for i in range(length - 1) if digits[i] == digits[i+1])
    score -= pairs

    score = max(1, min(score, 10))

    if score >= 8:
        label = "🟢 Strong"
    elif score >= 5:
        label = "🟡 Moderate"
    else:
        label = "🟠 Weak"

    return {"score": score, "label": label, "reason": ""}

# ── CLI ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🔐 Secure PIN Generator",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    gen_parser = subparsers.add_parser("generate", aliases=["g"], help="Generate a PIN")
    gen_parser.add_argument("-l", "--length", type=int, choices=[4, 6, 8], default=4,
                            help="PIN length: 4, 6, or 8 (default: 4)")
    gen_parser.add_argument("-n", "--count", type=int, default=5,
                            help="Number of PINs to generate (default: 5)")

    chk_parser = subparsers.add_parser("check", aliases=["c"], help="Check your own PIN")
    chk_parser.add_argument("pin", type=str, help="PIN to check")

    args = parser.parse_args()

    if args.command in ("generate", "g"):
        print(f"\n🔐 Secure {args.length}-digit PINs:\n")
        for i in range(args.count):
            print(f"  {i+1}. {generate_pin(args.length)}")
        print()

    elif args.command in ("check", "c"):
        result = score_pin(args.pin)
        print(f"\n🔍 PIN check: {'*' * len(args.pin)}")
        print(f"   {result['label']}  ({result['score']}/10)")
        if result["reason"]:
            print(f"   Reason: {result['reason']}")
        print()

    else:
        print("\n🔐 Secure PINs (4 digits):\n")
        for i in range(5):
            print(f"  {i+1}. {generate_pin(4)}")
        print('\nTip: use "python pin_gen.py --help" for all options\n')

if __name__ == "__main__":
    main()
