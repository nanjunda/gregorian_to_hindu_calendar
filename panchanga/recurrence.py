from datetime import datetime, timedelta
import pytz
from utils.astronomy import get_sidereal_longitude, get_sunrise_sunset, sun, moon, get_previous_new_moon
from panchanga.calculations import (
    calculate_tithi, calculate_masa_samvatsara, calculate_vara, 
    calculate_nakshatra, calculate_yoga, calculate_karana, format_panchanga_report
)

def find_recurrences(base_dt, loc_details, num_years=20):
    """
    Finds the next num_years occurrences of the same Masa, Paksha, and Tithi.
    Starts search from the current year.
    """
    # 1. Get target attributes from the original date
    utc_dt = base_dt.astimezone(pytz.utc)
    sun_lon = get_sidereal_longitude(utc_dt, sun)
    moon_lon = get_sidereal_longitude(utc_dt, moon)
    
    target_tithi, target_paksha = calculate_tithi(sun_lon, moon_lon)
    
    # Target Masa must be determined at the New Moon preceding the original event
    prev_nm_utc = get_previous_new_moon(utc_dt)
    sun_lon_at_nm = get_sidereal_longitude(prev_nm_utc, sun)
    target_masa, _ = calculate_masa_samvatsara(base_dt.year, sun_lon_at_nm, sun_lon)
    
    current_year = datetime.now().year
    print(f"Searching for: {target_masa}, {target_paksha}, {target_tithi} starting from {current_year}")
    
    results = []
    
    # 2. Iterate through future years starting from current_year
    for year_offset in range(num_years + 1):
        year = current_year + year_offset
        # Approximate date: use same month/day from original input as starting point for search
        try:
            approx_date = datetime(year, base_dt.month, base_dt.day, base_dt.hour, base_dt.minute)
        except ValueError:
            # Handle Feb 29
            approx_date = datetime(year, base_dt.month, base_dt.day - 1, base_dt.hour, base_dt.minute)
            
        # Search window +/- 30 days
        found_for_year = False
        start_search = approx_date - timedelta(days=32)
        
        # Scan day by day
        for d_offset in range(65): # 65 days window to be safe
            current_day = start_search + timedelta(days=d_offset)
            current_day_local = current_day.replace(tzinfo=None) # naive for calculation
            
            # For each day, we check the Panchanga elements at the input time or noon
            # Traditionally, we should check when the Tithi prevails.
            # Here we check the exact same time of day as the original input.
            tz = pytz.timezone(loc_details["timezone"])
            dt_local = tz.localize(datetime(current_day.year, current_day.month, current_day.day, base_dt.hour, base_dt.minute))
            dt_utc = dt_local.astimezone(pytz.utc)
            
            s_lon = get_sidereal_longitude(dt_utc, sun)
            m_lon = get_sidereal_longitude(dt_utc, moon)
            
            tithi, paksha = calculate_tithi(s_lon, m_lon)
            
            # For each candidate day, we must also check the Masa at THAT day's preceding New Moon
            curr_nm_utc = get_previous_new_moon(dt_utc)
            s_lon_at_nm = get_sidereal_longitude(curr_nm_utc, sun)
            masa, samvatsara = calculate_masa_samvatsara(dt_local.year, s_lon_at_nm, s_lon)
            
            if tithi == target_tithi and paksha == target_paksha and masa == target_masa:
                # Found the match!
                # Calculate full details for report
                sunrise, sunset = get_sunrise_sunset(dt_local, loc_details["latitude"], loc_details["longitude"], loc_details["timezone"])
                vara = calculate_vara(dt_local, sunrise)
                nakshatra = calculate_nakshatra(m_lon)
                yoga = calculate_yoga(s_lon, m_lon)
                karana = calculate_karana(s_lon, m_lon)
                
                report = format_panchanga_report(
                    dt_local, loc_details["address"], loc_details["timezone"],
                    sunrise, sunset, samvatsara, masa, paksha, tithi,
                    vara, nakshatra, yoga, karana
                )
                
                results.append({
                    "datetime": dt_local,
                    "report": report
                })
                found_for_year = True
                break
                
    return results
