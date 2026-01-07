import os
import abc
import google.generativeai as genai

class BaseAIEngine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_insight(self, config_data):
        pass

class GeminiEngine(BaseAIEngine):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Upgraded to Gemini 2.5 Flash (v5.0 high-intelligence edition)
            self.model_name = 'gemini-2.5-flash'
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
            self.model_name = None

    def generate_insight(self, config_data):
        if not self.model:
            return "AI Engine not configured. Please set GOOGLE_API_KEY environment variable."

        # Extracting data for the prompt
        samvatsara = config_data.get('samvatsara')
        masa = config_data.get('masa')
        paksha = config_data.get('paksha')
        tithi = config_data.get('tithi')
        nakshatra = config_data.get('nakshatra')
        yoga = config_data.get('yoga')
        karana = config_data.get('karana')
        location = config_data.get('address')
        input_dt = config_data.get('input_datetime')
        
        # Split datetime if possible for cleaner prompt
        date_part, time_part = "N/A", "N/A"
        if input_dt and ' ' in input_dt:
            date_part, time_part = input_dt.split(' ', 1)
        elif input_dt:
            date_part = input_dt

        prompt = f"""
        Role: The "Astro-Tutor" (An expert in Astronomy, Math, and Mythology who speaks the language of middle and high school students).

        Objective:
        Generate a comprehensive Panchanga report for this specific moment. Bridge the gap between Ancient Indian Astronomy and Modern Science. Retain high-level technical details but explain them using relatable analogies (geometry, sports, clockwork, coding).

        Input Data:
        - Date: {date_part}
        - Time: {time_part}
        - Location: {location}
        - Samvatsara: {samvatsara}
        - Masa: {masa}
        - Paksha: {paksha}
        - Tithi: {tithi}
        - Nakshatra: {nakshatra}
        - Yoga: {yoga}
        - Karana: {karana}

        Instructions for Output Structure:

        1. Introduction: The "Time-Keeping" Engine
        - Explain what a calendar actually is.
        - Introduce the Western (Solar) vs. Hindu Panchanga (Lunisolar) systems.

        2. The Code: Western vs. Hindu Systems
        - Highlight differences: Tropical Zodiac (Western/Seasons) vs. Sidereal Zodiac (Hindu/Fixed Stars).
        - Explain the "Start of Day" (Midnight vs. Sunrise).

        3. The "Birthday Algorithm" (The 11-Day Gap)
        - Explain why an Indian birthday differs from a Western birthday.
        - Show the math: Solar Year (365.25 days) - Lunar Year (354 days) = ~11 days difference.
        - Explain the "drift" and how Adhika Masa (Leap Month) fixed it.

        4. The Deep Dive (The Result Analysis)
        - Section A: The Astronomer’s Snapshot (Geometry) -> Explain Tithi (Angle), Nakshatra (Coordinates/Star), Yoga, and Karana using the input data above.
        - Section B: The Physicist’s Lab (Mechanics) -> Explain Orbital Periods (Synodic vs. Sidereal) and Precession.
        - Section C: The Storyteller’s Archive (Myth) -> Connect the astronomy to the mythology (Deities, Vibes, Stories) for these specific results.

        5. The Cosmic Cheat Sheet (Vocabulary)
        - Define: Equinox, Precession, and Epoch using simple analogies (spinning tops, video game save points, seesaws).

        Tone: Encouraging, precise, visual, and educational. Use Markdown formatting. Use the term 'Panchanga' instead of 'Vedic'.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Multi-stage Fallback (v5.0 robustness for 2026)
            # We try the newest models first, cascading down to legacy versions.
            fallback_models = [
                'gemini-3-flash',        # Latest 2026 model
                'gemini-2.5-flash',      # High-performance 2025/26 stable
                'gemini-2.5-flash-latest', 
                'gemini-2.0-flash',      # Stable 2.0 release
                'gemini-1.5-flash'       # Legacy safety net
            ]
            
            for fallback_name in fallback_models:
                if fallback_name == self.model_name:
                    continue
                    
                try:
                    print(f"Model {self.model_name} failed. Attempting fallback to {fallback_name}...")
                    fallback_model = genai.GenerativeModel(fallback_name)
                    response = fallback_model.generate_content(prompt)
                    return response.text
                except Exception:
                    continue
            
            return f"Error generating insight: {str(e)}"

# Factory or Manager to handle future expansion
class AIEngineManager:
    def __init__(self, provider="gemini"):
        if provider == "gemini":
            self.engine = GeminiEngine()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    def get_explanation(self, config_data):
        return self.engine.generate_insight(config_data)

# Singleton instance for easy import
ai_engine = AIEngineManager()
