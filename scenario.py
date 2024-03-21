
# scenario.py
class Scenario:
    def __init__(self, number, ID, color, glider_file, start_alt, end_alt, airspeed, headwind_correction, AS_VV_correction, drag_scale, air_vv, winds):
        self.scenario_number = number
        self.ID = ID
        self.color = color
        self.glider_file = glider_file
        self.start_altitude = start_alt
        self.end_altitude = end_alt
        self.base_airspeed = airspeed
        self.headwind_correction = headwind_correction
        self.AS_due_VV_correction = AS_VV_correction
        self.drag_scale = drag_scale
        self.airmass_vv = air_vv
        self.winds = winds

    
