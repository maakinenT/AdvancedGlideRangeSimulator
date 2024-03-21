
# scenario.py
class Scenario:
    def __init__(self, number, ID, color, glider_file, start_alt, end_alt, headwind_correction, air_vv, winds):
        self.scenario_number = number
        self.ID = ID
        self.color = color
        self.glider_file = glider_file
        self.start_altitude = start_alt
        self.end_altitude = end_alt
        self.headwind_correction = headwind_correction
        self.airmass_vv = air_vv
        self.winds = winds

    
