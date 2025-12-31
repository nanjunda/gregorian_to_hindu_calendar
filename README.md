# Hindu Panchanga Converter v2.0

A high-precision tool to convert Gregorian calendar dates, times, and locations into traditional Hindu Panchanga elements (Tithi, Nakshatra, Yoga, Karana, Vara, Masa, and Samvatsara).

## Features
- **Version 2.0 (New):**
    - **Vedic Recurrence:** Generate calendar events that recur based on Masa, Paksha, and Tithi.
    - **iCal Export:** Download a 10-year `.ics` file for easy import into digital calendars.
    - **Detailed Reports:** Every calendar event includes a full ASCI Panchanga report in the description.
- **Web UI:** Modern, responsive interface with glassmorphism design.
- **CLI Utility:** Command-line tool for quick conversions.
- **High Precision:** Uses `skyfield` for astronomical data and Lahiri Ayanamsha.
- **Geolocation:** Automatic location resolution and timezone handling.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd gregorian_to_hindu_calendar
   ```

2. **Setup virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Web UI:**
   ```bash
   python3 app.py
   ```
   Access it at `http://127.0.0.1:8080`.

4. **Run the CLI:**
   ```bash
   python3 panchanga_converter.py --date 2025-12-30 --time 16:17 --location "Bangalore, India"
   ```

## Documentation
Refer to the `docs/` directory for architecture, implementation plans, and walkthroughs.
