# One-Pager: Gregorian to Hindu Panchanga Converter

## Objective
To develop a Python script that accurately converts a Gregorian calendar date (Year, Month, Day, 24-hour Time) and location (City, State, Country) into its corresponding Hindu Panchanga elements.

## Scope of Calculations
The script will calculate and display the following "Five Limbs" (and associated details):
1.  **Vara (Weekday):** Solar weekday based on the 24-hour cycle.
2.  **Tithi (Lunar Day):** Determined by the angular distance between the Sun and the Moon.
    *   Includes **Paksha** (Shukla - Bright, Krishna - Dark).
3.  **Nakshatra (Lunar Mansion):** The constellation where the Moon is positioned.
4.  **Masa (Lunar Month):** The lunar month name (e.g., Chaitra, Vaishakha).
5.  **Samvatsara:** The name of the year in the 60-year Jovian cycle (e.g., Krodhi, Vishvavasu).

*Note: Yoga and Karana will be included in the implementation as they are core limbs of the Panchanga.*

## Technical Approach
*   **Precision and Location:** Hindu Panchanga calculations are highly dependent on the observer's location (specifically for calculating Sunrise, which is the baseline for many Panchanga elements). The script will include a Geolocation component to resolve City/State/Country into Latitude, Longitude, and Timezone.
*   **Ayanamsha:** Accurate calculation of astronomical elements like Nakshatra and Tithi requires handling Ayanamsha (e.g., Lahiri), which is the difference between Tropical and Sidereal zodiacs.
*   **Libraries:** Utilization of robust Python libraries such as `skyfield` or `pyswisseph` for planetary ephemeris data, and `geopy` for location resolution.

## Deliverables
1.  **Architecture Document:** Detailed design of the computation engine.
2.  **Implementation Plan:** Step-by-step coding and verification stages.
3.  **Python Script:** The final executable tool.

## Acceptance Criteria
*   Input format: YYYY, MM, DD, HH:MM and Location (City, State, Country).
*   Output format: Clear text representation of all Panchanga elements (Vara, Tithi, Nakshatra, Yoga, Karana, Masa, Samvatsara).
*   Verification: Cross-checking results with established Panchanga sources (e.g., Drik Panchang) for specific locations.
