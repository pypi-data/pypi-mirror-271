import os
import json
import platform

class PreferenceLogic:
    def __init__(self) -> None:
        pass

    def set_preference(
            self,
            preference_name, 
            preference_value
        ):
        # Determine the user's home directory based on their operating system
        home_dir = os.path.expanduser("~")
        preferences_file = os.path.join(home_dir, "gmax_preferences.json")

        # Load existing preferences if the file exists
        if os.path.exists(preferences_file):
            with open(preferences_file, 'r') as file:
                preferences = json.load(file)
        else:
            preferences = {}

        # Update the preference
        preferences[preference_name] = preference_value
        # Save the updated preferences back to the file
        with open(preferences_file, 'w') as file:
            json.dump(preferences, file, indent=4)

    def get_preference(
            self,
            preference_name
        ):
        # Determine the user's home directory
        home_dir = os.path.expanduser("~")
        preferences_file = os.path.join(home_dir, "gmax_preferences.json")

        # Check if the preferences file exists
        if not os.path.exists(preferences_file):
            return None

        # Load the preferences
        with open(preferences_file, 'r') as file:
            preferences = json.load(file)

        # Retrieve the requested preference
        return preferences.get(preference_name, None)