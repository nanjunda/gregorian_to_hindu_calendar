from skyfield.api import load, Topos, Star
from skyfield import almanac
from datetime import datetime, timedelta
import pytz
import numpy as np

# Load ephemeris data
eph = load('de421.bsp')
sun = eph['sun']
moon = eph['moon']
earth = eph['earth']
ts = load.timescale()

def get_ayanamsha(jd):
    """
    Calculates Lahiri Ayanamsha for a given Julian Date.
    Simple linear approximation: 
    23.85 degrees at J2000.0 + 50.27 seconds per year.
    Reference: J2000.0 corresponds to JD 2451545.0
    """
    t = (jd - 2451545.0) / 36525.0 # Centuries from J2000.0
    # Lahiri Ayanamsha formula (approximate)
    ayanamsha = 23.8580833 + (50.2785 * t / 36) # 50.2785 per year
    return ayanamsha

def get_sidereal_longitude(target_time_utc, body):
    """
    Calculates the Nirayana (Sidereal) longitude of a celestial body (Sun or Moon).
    """
    t = ts.from_datetime(target_time_utc)
    astrometric = earth.at(t).observe(body)
    ecliptic_lat, ecliptic_lon, distance = astrometric.ecliptic_latlon()
    
    tropical_lon = ecliptic_lon.degrees
    ayanamsha = get_ayanamsha(t.tt)
    
    sidereal_lon = (tropical_lon - ayanamsha) % 360
    return sidereal_lon

def get_sunrise_sunset(date_local, lat, lon, timezone_str):
    """
    Calculates Sunrise and Sunset for a given date and location.
    """
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    tz = pytz.timezone(timezone_str)
    
    # Define the time range for the day (searching from 00:00 to 23:59 local)
    t0 = ts.from_datetime(tz.localize(datetime(date_local.year, date_local.month, date_local.day, 0, 0, 0)))
    t1 = ts.from_datetime(tz.localize(datetime(date_local.year, date_local.month, date_local.day, 23, 59, 59)))
    
    f = almanac.sunrise_sunset(eph, Topos(latitude_degrees=lat, longitude_degrees=lon))
    times, events = almanac.find_discrete(t0, t1, f)
    
    sunrise = None
    sunset = None
    
    for t, event in zip(times, events):
        if event == 1: # Sunrise
            sunrise = t.astimezone(tz)
        elif event == 0: # Sunset
            sunset = t.astimezone(tz)
            
    return sunrise, sunset

if __name__ == "__main__":
    # Test
    now_utc = datetime.now(pytz.utc)
    sun_lon = get_sidereal_longitude(now_utc, sun)
    moon_lon = get_sidereal_longitude(now_utc, moon)
    print(f"Sun Sidereal Longitude: {sun_lon}")
    print(f"Moon Sidereal Longitude: {moon_lon}")
    
    # Test sunrise
    sr, ss = get_sunrise_sunset(datetime.now(), 12.9716, 77.5946, "Asia/Kolkata")
    print(f"Sunrise: {sr}")
    print(f"Sunset: {ss}")
