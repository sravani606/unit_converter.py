"""
converter.py
Core conversion logic for the Unit Converter tool. Pure Python, no
external dependencies.

Supports:
- Length
- Weight / mass
- Temperature (Celsius, Fahrenheit, Kelvin)
- Volume
- Time

Most categories convert via a common base unit (e.g. metres for length).
Temperature requires special-case formulas since it isn't a simple
multiplicative conversion.
"""

from typing import Dict, List

# Each category maps a unit name (and common aliases) to how many of the
# category's BASE UNIT one unit of that name equals.
# e.g. for length, base unit = metre. 1 km = 1000 m, so "km": 1000.

LENGTH_UNITS: Dict[str, float] = {
    "mm": 0.001,
    "millimeter": 0.001,
    "millimeters": 0.001,
    "cm": 0.01,
    "centimeter": 0.01,
    "centimeters": 0.01,
    "m": 1.0,
    "meter": 1.0,
    "meters": 1.0,
    "km": 1000.0,
    "kilometer": 1000.0,
    "kilometers": 1000.0,
    "in": 0.0254,
    "inch": 0.0254,
    "inches": 0.0254,
    "ft": 0.3048,
    "foot": 0.3048,
    "feet": 0.3048,
    "yd": 0.9144,
    "yard": 0.9144,
    "yards": 0.9144,
    "mi": 1609.344,
    "mile": 1609.344,
    "miles": 1609.344,
}

WEIGHT_UNITS: Dict[str, float] = {
    "mg": 0.001,
    "milligram": 0.001,
    "milligrams": 0.001,
    "g": 1.0,
    "gram": 1.0,
    "grams": 1.0,
    "kg": 1000.0,
    "kilogram": 1000.0,
    "kilograms": 1000.0,
    "oz": 28.349523125,
    "ounce": 28.349523125,
    "ounces": 28.349523125,
    "lb": 453.59237,
    "lbs": 453.59237,
    "pound": 453.59237,
    "pounds": 453.59237,
    "tonne": 1_000_000.0,
    "tonnes": 1_000_000.0,
    "ton": 907184.74,
    "tons": 907184.74,
}

VOLUME_UNITS: Dict[str, float] = {
    "ml": 0.001,
    "milliliter": 0.001,
    "milliliters": 0.001,
    "l": 1.0,
    "liter": 1.0,
    "liters": 1.0,
    "litre": 1.0,
    "litres": 1.0,
    "cup": 0.236588,
    "cups": 0.236588,
    "tbsp": 0.0147868,
    "tablespoon": 0.0147868,
    "tablespoons": 0.0147868,
    "tsp": 0.00492892,
    "teaspoon": 0.00492892,
    "teaspoons": 0.00492892,
    "gal": 3.78541,
    "gallon": 3.78541,
    "gallons": 3.78541,
    "qt": 0.946353,
    "quart": 0.946353,
    "quarts": 0.946353,
    "pt": 0.473176,
    "pint": 0.473176,
    "pints": 0.473176,
    "floz": 0.0295735,
    "fl_oz": 0.0295735,
}

TIME_UNITS: Dict[str, float] = {
    "ms": 0.001,
    "millisecond": 0.001,
    "milliseconds": 0.001,
    "s": 1.0,
    "sec": 1.0,
    "second": 1.0,
    "seconds": 1.0,
    "min": 60.0,
    "minute": 60.0,
    "minutes": 60.0,
    "h": 3600.0,
    "hr": 3600.0,
    "hour": 3600.0,
    "hours": 3600.0,
    "day": 86400.0,
    "days": 86400.0,
    "week": 604800.0,
    "weeks": 604800.0,
}

TEMPERATURE_UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}

CATEGORIES = {
    "length": LENGTH_UNITS,
    "weight": WEIGHT_UNITS,
    "volume": VOLUME_UNITS,
    "time": TIME_UNITS,
}


class ConversionError(Exception):
    """Raised for unrecognized units or incompatible conversions."""


def _normalize(unit: str) -> str:
    return unit.strip().lower()


def find_category(unit: str) -> str:
    """Return the category name a unit belongs to, or raise ConversionError."""
    unit = _normalize(unit)
    if unit in TEMPERATURE_UNITS:
        return "temperature"
    for category, table in CATEGORIES.items():
        if unit in table:
            return category
    raise ConversionError(f"Unrecognized unit: '{unit}'")


def list_units(category: str) -> List[str]:
    """Return the canonical (non-alias) unit list for a category, for display."""
    canonical = {
        "length": ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"],
        "weight": ["mg", "g", "kg", "oz", "lb", "ton", "tonne"],
        "volume": ["ml", "l", "cup", "tbsp", "tsp", "gal", "qt", "pt", "floz"],
        "time": ["ms", "s", "min", "h", "day", "week"],
        "temperature": ["c", "f", "k"],
    }
    if category not in canonical:
        raise ConversionError(f"Unknown category: '{category}'")
    return canonical[category]


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = _normalize(from_unit)
    to_unit = _normalize(to_unit)

    # Normalize aliases to c/f/k
    alias = {"celsius": "c", "fahrenheit": "f", "kelvin": "k"}
    from_unit = alias.get(from_unit, from_unit)
    to_unit = alias.get(to_unit, to_unit)

    if from_unit not in ("c", "f", "k") or to_unit not in ("c", "f", "k"):
        raise ConversionError(f"Unrecognized temperature unit(s): '{from_unit}', '{to_unit}'")

    # Convert from_unit -> Celsius
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:  # kelvin
        celsius = value - 273.15

    # Convert Celsius -> to_unit
    if to_unit == "c":
        return celsius
    elif to_unit == "f":
        return celsius * 9 / 5 + 32
    else:  # kelvin
        return celsius + 273.15


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert `value` from `from_unit` to `to_unit`.

    Raises ConversionError if either unit is unrecognized, or if the
    two units belong to different categories (e.g. metres to kilograms).
    """
    from_category = find_category(from_unit)
    to_category = find_category(to_unit)

    if from_category != to_category:
        raise ConversionError(
            f"Cannot convert between incompatible units: "
            f"'{from_unit}' ({from_category}) and '{to_unit}' ({to_category})"
        )

    if from_category == "temperature":
        return _convert_temperature(value, from_unit, to_unit)

    table = CATEGORIES[from_category]
    from_key = _normalize(from_unit)
    to_key = _normalize(to_unit)

    base_value = value * table[from_key]
    return base_value / table[to_key]
