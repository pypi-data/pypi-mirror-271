import json
import os

# Path to the directory containing this script
PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))

def get_universities():
    """
    Retrieve the list of universities along with their state codes.
    """
    with open(os.path.join(PACKAGE_DIR, 'universities_data.json'), 'r') as file:
        universities_data = json.load(file)
    return universities_data

def get_state_code_of_university(university):
    """
    Get the state code for a given university.
    """
    universities = get_universities()
    for uni, state in universities.items():
        if university.lower() in uni.lower():
            return {uni: state}
    return {}

def get_universities_by_state_code(state_code):
    """
    Get a list of universities located in a specific state.
    """
    universities = get_universities()
    state_universities = {uni: state for uni, state in universities.items() if state == state_code}
    return state_universities
