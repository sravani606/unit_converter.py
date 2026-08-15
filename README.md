# 🔁 Unit Converter

**Intern ID:** CITS8111

A command-line unit converter written in pure Python — **no external
dependencies**. Convert between units of length, weight, volume, time,
and temperature.

## Features

- 📏 **Length** — mm, cm, m, km, inches, feet, yards, miles
- ⚖️ **Weight** — mg, g, kg, oz, lb, ton, tonne
- 🧪 **Volume** — ml, l, cup, tbsp, tsp, gallon, quart, pint, fl oz
- ⏱️ **Time** — ms, s, min, hour, day, week
- 🌡️ **Temperature** — Celsius, Fahrenheit, Kelvin (proper formula-based conversion, not just multiplication)
- Case-insensitive unit names, with common aliases (`km` / `kilometer` / `kilometers`)
- Clear error messages for invalid or incompatible units (e.g. converting km to kg)
- Interactive mode for converting multiple values in a row
- Single-shot command-line mode for quick lookups or scripting

## Installation

```bash
git clone https://github.com/<your-username>/unit-converter.git
cd unit-converter
