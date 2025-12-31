# Architecture: Hindu Panchanga Converter

## Overview
The "Gregorian to Hindu Panchanga Converter" is designed as a modular Python application. It separates data acquisition (ephemeris and geolocation), astronomical computations, and Vedic calendrical logic.

## System Components

```mermaid
graph TD
    User["User Interface (Web Browser)"] --> Frontend["HTML/CSS/JS Frontend"]
    Frontend --> Flask["Flask Backend API"]
    
    Flask --> Geocoder["Geolocation Engine (GeoPy/Browser API)"]
    Geocoder --> LatLong["Latitude, Longitude, Timezone"]
    
    Flask --> AstroEngine["Astronomical Engine (Skyfield)"]
    
    AstroEngine --> Longitudes["Sun & Moon Longitudes"]
    LatLong --> SunriseCalc["Sunrise/Sunset Calculator"]
    
    Longitudes --> PanchangaLogic["Panchanga Computation Logic"]
    SunriseCalc --> PanchangaLogic
    
    PanchangaLogic --> Tithi["Tithi & Paksha"]
    PanchangaLogic --> Vara["Vara"]
    PanchangaLogic --> Nakshatra["Nakshatra"]
    PanchangaLogic --> YogaKarana["Yoga & Karana"]
    PanchangaLogic --> MasaSamvat["Masa & Samvatsara"]
    
    Tithi & Vara & Nakshatra & YogaKarana & MasaSamvat --> Formatter["JSON Formatter"]
    Formatter --> Frontend
    Frontend --> FinalOutput["Responsive Output Display"]
```

## Module Descriptions

### 1. Geolocation Engine
*   **Purpose:** Converts human-readable location strings (e.g., "Bangalore, KA, India") into Geographic Coordinates.
*   **Technology:** `geopy` and `timezonefinder`.

### 2. Astronomical Engine
*   **Purpose:** High-precision computation of planetary positions.
*   **Technology:** `skyfield` (Pure Python astronomy library).
*   **Key Tasks:** Calculate the positioning of the Sun and Moon to derive longitudes for Panchanga elements with Lahiri Ayanamsha support.

### 3. Panchanga Computation Logic
*   **Tithi:** (Moon Longitude - Sun Longitude) / 12°.
*   **Vara:** Determined based on the day of the week, adjusted for sunrise if necessary (traditional Vedic day starts at sunrise).
*   **Nakshatra:** Moon Longitude / (360° / 27).
*   **Yoga:** (Sun Longitude + Moon Longitude) / (360° / 27).
*   **Karana:** Half of a Tithi (6°).
*   **Masa:** Based on the Sun's entry into Rasis (Sankranti) and the Tithi at the time of New Moon.
*   **Samvatsara:** Determined from the 60-year Jovian cycle.

### 4. Web Interface & Backend
*   **Web Server:** Flask framework to handle HTTP requests and serve the UI.
*   **Frontend:** A responsive single-page application (SPA) built with HTML5, CSS3 (Vanilla), and JavaScript.
*   **Output Formatter:** Transforms numerical results into JSON for consumption by the frontend.

## Data Flow
1.  **Input:** User provides date/time and location.
2.  **Normalization:** Resolve coordinates and calculate the local sunrise for that specific day.
3.  **Compute:** Calculate the Sidereal longitudes for the target time.
4.  **Derive:** Apply Vedic formulas to the astronomical data.
5.  **Present:** Display the results in a readable format.

## User Review Required
> [!NOTE]
> I have switched from `pyswisseph` to `skyfield` because `pyswisseph` encountered compilation errors on Python 3.14. `skyfield` is a pure Python library that provides high-precision astronomical calculations and is fully compatible with your environment.
> I will use **Lahiri Ayanamsha** as the default, as it is the standard for most Indian Panchangas.
