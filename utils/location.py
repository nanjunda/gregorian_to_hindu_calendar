from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

def get_location_details(location_name):
    """
    Given a city/location name, returns lat, lon, and timezone.
    """
    geolocator = Nominatim(user_agent="hindu_panchanga_converter")
    location = geolocator.geocode(location_name)
    
    if not location:
        raise ValueError(f"Could not find location: {location_name}")
    
    lat = location.latitude
    lon = location.longitude
    
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    
    if not timezone_str:
         raise ValueError(f"Could not find timezone for location: {location_name}")
         
    return {
        "address": location.address,
        "latitude": lat,
        "longitude": lon,
        "timezone": timezone_str
    }

if __name__ == "__main__":
    # Test
    try:
        details = get_location_details("Bangalore, India")
        print(details)
    except Exception as e:
        print(f"Error: {e}")
