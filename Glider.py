import numpy

# Glider.py
class Glider:
    def __init__(self, name, mass, min_sink, min_sink_at, best_glide, best_glide_at, polar_AS, polar_VV):
        self.name = name
        self.mass = mass
        self.drag_polar_AS = polar_AS
        self.drag_polar_VV = polar_VV
        self.min_sink = min_sink
        self.min_sink_at = min_sink_at
        self.best_glide = best_glide
        self.best_glide_at = best_glide_at

    def sinkAtAirspeed(self, AS):
        vv = numpy.interp(AS, self.drag_polar_AS, self.drag_polar_VV, left=None, right=None, period=None)
        return vv
    
