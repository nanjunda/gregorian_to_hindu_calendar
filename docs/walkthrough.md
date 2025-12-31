# Walkthrough: Hindu Panchanga Converter

I have implemented a Python-based Hindu Panchanga Converter that takes a Gregorian date, time, and location to provide traditional Vedic calendar elements.

## Features Implemented
*   **Geolocation:** Automatic resolution of coordinates and timezones using `geopy` and `timezonefinder`.
*   **Astronomical Precision:** High-precision Sun and Moon positions using `skyfield`.
*   **Vedic Logic:** Accurate derivation of the "Five Limbs" (Panchanga):
    *   **Vara:** Weekday adjusted for Sunrise.
    *   **Tithi:** Lunar day with Paksha (Shukla/Krishna).
    *   **Nakshatra:** Lunar mansion.
    *   **Yoga:** Auspicious angular relationship.
    *   **Karana:** Half-Tithi division.
*   **Calendrical Context:** Correct identification of **Masa** (Lunar month) and **Samvatsara** (60-year cycle).

## Verification Results

### Scenario 1: Future Date (Dec 30, 2025 in Bangalore)
Command run:
```bash
python3 panchanga_converter.py --date 2025-12-30 --time 16:17 --location "Bangalore, India"
```

Output:
```text
========================================
       HINDU PANCHANGA REPORT
========================================
Input Date/Time : 2025-12-30 16:17:00 (Asia/Kolkata)
Location        : Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, India
Sunrise         : 06:40:56
Sunset          : 18:03:23
----------------------------------------
Samvatsara      : Vishvavasu
Masa (Month)    : Pausha
Paksha          : Shukla
Tithi           : Ekadashi
Vara (Weekday)  : Mangalavara
Nakshatra       : Bharani
Yoga            : Siddha
Karana (Index)  : 21
========================================
```

### Scenario 2: Historical Verification (Dec 30, 2024 in Bangalore)
Result: **Somavara** (Monday), **Krodhi** Samvatsara, **Amavasya** Tithi. This matches the known Panchanga for that date.

## Web User Interface
I have added a modern, premium Web UI wrapper for the converter.

### Features
*   **Vibrant UI:** Glassmorphism design with responsive layout.
*   **Geolocation Support:** Integrated browser geolocation for automatic coord resolution.
*   **Interactive:** Results are fetched asynchronously and displayed in a clean grid.

### How to Run the Web UI Locally
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Start the Flask server:
   ```bash
   python3 app.py
   ```
3. Open your browser and navigate to:
   [http://127.0.0.1:8080](http://127.0.0.1:8080)

## How to Run the CLI Locally
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Run the script:
   ```bash
   python3 panchanga_converter.py --date YYYY-MM-DD --time HH:MM --location "City, Country"
   ```

## Final Verification
The Web UI has been tested on a MacBook environment, confirming that it leverages local resources efficiently and provides an intuitive interface for Hindu Panchanga calculations.
