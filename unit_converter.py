#!/usr/bin/env python3
"""
unit_converter.py
Command-line unit converter. Pure Python, no external dependencies.

Usage:
    python unit_converter.py 10 km m
    python unit_converter.py 100 celsius fahrenheit
    python unit_converter.py 2.5 gal l
    python unit_converter.py --list length
    python unit_converter.py            # interactive mode
"""

import argparse
import sys

from converter import convert, list_units, find_category, ConversionError, CATEGORIES


def print_units_table():
    print("Available units by category:\n")
    for category in list(CATEGORIES.keys()) + ["temperature"]:
        units = list_units(category)
        print(f"  {category:<12} {', '.join(units)}")
    print()


def run_conversion(value: float, from_unit: str, to_unit: str) -> int:
    try:
        result = convert(value, from_unit, to_unit)
    except ConversionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"{value} {from_unit} = {result:g} {to_unit}")
    return 0


def interactive_mode() -> int:
    print("Unit Converter (interactive mode). Type 'quit' to exit, 'units' to list units.\n")
    while True:
        try:
            raw = input("Convert (e.g. '10 km m'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not raw:
            continue
        if raw.lower() in ("quit", "exit", "q"):
            return 0
        if raw.lower() == "units":
            print_units_table()
            continue

        parts = raw.split()
        if len(parts) != 3:
            print("Please enter: <value> <from_unit> <to_unit>  (e.g. '10 km m')")
            continue

        value_str, from_unit, to_unit = parts
        try:
            value = float(value_str)
        except ValueError:
            print(f"'{value_str}' is not a valid number.")
            continue

        try:
            result = convert(value, from_unit, to_unit)
            print(f"  -> {value} {from_unit} = {result:g} {to_unit}\n")
        except ConversionError as exc:
            print(f"  Error: {exc}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unit_converter",
        description="Convert values between units of length, weight, volume, time, and temperature.",
    )
    parser.add_argument("value", nargs="?", type=float, help="Numeric value to convert")
    parser.add_argument("from_unit", nargs="?", help="Unit to convert from (e.g. km)")
    parser.add_argument("to_unit", nargs="?", help="Unit to convert to (e.g. m)")
    parser.add_argument(
        "--list",
        metavar="CATEGORY",
        help="List available units for a category "
             "(length, weight, volume, time, temperature) and exit",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        try:
            units = list_units(args.list.lower())
        except ConversionError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"{args.list}: {', '.join(units)}")
        return 0

    if args.value is not None and args.from_unit and args.to_unit:
        return run_conversion(args.value, args.from_unit, args.to_unit)

    if args.value is not None or args.from_unit or args.to_unit:
        parser.error("Provide all three of: value, from_unit, to_unit")

    return interactive_mode()


if __name__ == "__main__":
    sys.exit(main())
