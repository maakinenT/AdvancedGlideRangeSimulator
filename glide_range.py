#    _       _                               _    ____ _ _     _
#   / \   __| |_   ____ _ _ __   ___ ___  __| |  / ___| (_) __| | ___
#  / _ \ / _` \ \ / / _` | '_ \ / __/ _ \/ _` | | |  _| | |/ _` |/ _ \
# / ___ \ (_| |\ V / (_| | | | | (_|  __/ (_| | | |_| | | | (_| |  __/
#/_/__ \_\__,_| \_/ \__,_|_| |_|\___\___|\__,_|  \____|_|_|\__,_|\___|
#|  _ \ __ _ _ __   __ _  ___  / ___|(_)_ __ ___  _   _| | __ _| |_ ___  _ __
#| |_) / _` | '_ \ / _` |/ _ \ \___ \| | '_ ` _ \| | | | |/ _` | __/ _ \| '__|
#|  _ < (_| | | | | (_| |  __/  ___) | | | | | | | |_| | | (_| | || (_) | |
#|_| \_\__,_|_| |_|\__, |\___| |____/|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|
#                  |___/
#
# (C) Tomi Mäkinen, 2024

# ---------------------------------- LIBRARIES AND FUNCTIONS ---------------------------------
# Import libraries
import gmplot
import numpy
import webbrowser
import matplotlib.pyplot as plt
import math
import numpy as np

# Import Classes and functions
from Glider import Glider
from scenario import Scenario
from GUI import GUI
from functions import relativePosToCoordinates
from functions import polarToCartesian
from functions import read_points_from_csv
from functions import plotDragPolars
from functions import plotAirfielCenteredLAR
from functions import plotDesiredTrackValues
from functions import plotOptimalFlightValues
from functions import plotPoints
from functions import printLogo
from functions import wind_components
from functions import draw_arrow
from functions import max_min_range_heading
# ----------------------------- END OF LIBRARIES AND FUNCTIONS --------------------------------

printLogo()

# ----------------------------------------- POINTS --------------------------------------------
EFJM = (61.781338, 22.710170)
EFPI = (61.245626, 22.193343)
# TODO: point from csv
# -------------------------------------- END OF POINTS ----------------------------------------


# ---------------------------------- CREATE SCENARIO DICT -------------------------------------
global scenarios
scenarios = {}
# ------------------------------ END OF CREATE SCENARIO DICT ----------------------------------



# --------------------------------------- GUI -------------------------------------------------
GUI(scenarios)    # store GUI inout in scenario dict (global)
# ------------------------------------ END OF GUI --------------------------------------------



# ------------------------------------- CREATING GLIDERS --------------------------------------
glider_filenames = []
color_list = []

for ID in scenarios:
  glider_filenames.append(scenarios[ID].glider_file)
  color_list.append(scenarios[ID].color)

# Create a dict of gliders
gliders_dict = {}

for file_name in glider_filenames:
  # read data from csv
  data, drag_polar = read_points_from_csv("gliders/"+str(file_name))

  drag_polar_airspeeds = []
  drag_polar_sink_rates = []

  for row in drag_polar:
    drag_polar_airspeeds.append(row[0])
    drag_polar_sink_rates.append(row[1])   

  # Create an glider object
  glider = Glider(data['name'],
                  float(data['mass']),
                  float(data['min_sink']),
                  float(data['min_sink_at']),
                  float(data['best_glide']),
                  float(data['best_glide_at']),
                  drag_polar_airspeeds,
                  drag_polar_sink_rates)

  gliders_dict[file_name] = glider        #use filename as key

# plot drag polar for every selected glider
plotDragPolars(gliders_dict, color_list)
# -------------------------------- END OF CREATING GLIDERS -------------------------------------


# -------------------------------------- SCENRIOS ----------------------------------------------

# Initialize figures where all skenarios will be plotted
LAR_figure, LAR_figure_ax = plt.subplots()  # Create LAR figure

desired_track_figure, desired_track_figure_ax = plt.subplots(5,1)  # Create desired track heading values figure
for ax in desired_track_figure_ax:
      ax.invert_xaxis()

for number in scenarios:    # Go through every scenario

  # ---------------------------------- SCENARIO PARAMETERS --------------------------------------
  selected_glider = gliders_dict[scenarios[number].glider_file]
  graph_color = scenarios[number].color
  # Convert RGB values to hexadecimal color code
  hex_color = "#{:02x}{:02x}{:02x}".format(int(graph_color[0]*255), int(graph_color[1]*255), int(graph_color[2]*255))
  end_altitude = scenarios[number].end_altitude
  selected_airspeed = scenarios[number].base_airspeed
  headwind_correction = scenarios[number].headwind_correction
  AS_due_VV_correction = scenarios[number].AS_due_VV_correction
  start_altitude = scenarios[number].start_altitude
  vertical_airmass_velocity = scenarios[number].airmass_vv
  winds = scenarios[number].winds   # Winds [(altitude_meters, speed_m/s, direction_degrees_TRUE)]

  airfield_location = EFJM
  dT = 1                        #s


  # print('SELECTED GLIDER:')
  # print('Name: ', selected_glider.name)
  # print('Min sink: ', selected_glider.min_sink, 'm/s at ', selected_glider.min_sink_at, 'km/h')
  # print('Best L/D: ', selected_glider.best_glide, ' at ', selected_glider.best_glide_at, 'km/h')

  # ------------------------------ END OF SCENARIO PARAMETERS -----------------------------------


  # ----------------------------- AIRFIELD CENTERED GLIDER RANGE --------------------------------
  winds_altitudes = []
  winds_speeds = []
  winds_directions = []

  for row in winds:
    winds_altitudes.append(row[0])
    winds_speeds.append(row[1])   
    winds_directions.append(row[2])   

  # SIMULATION

  glide_LAR = {}
  glide_values = {}
  X_pos_list = []
  y_pos_list = []

  for ground_track in range(0, 359, 10):

    altitude = start_altitude
    time = 0
    x_pos = 0
    y_pos = 0
    time_list = []
    airspeed_list = []
    groundspeed_list = []
    vv_list = []
    altitude_list = []
    LperD_list = []

    # Simulation of flight to given ground track direction
    while altitude > end_altitude:    # TODO: if positive VV, prevent infinite range 

      # linear interpolation
      wind_speed_at_altitude = numpy.interp(altitude, winds_altitudes, winds_speeds,
                                            left=None, right=None, period=None)
      wind_direction_at_altitude = numpy.interp(altitude, winds_altitudes, winds_directions,
                                            left=None, right=None, period=None)


      # calculate wind components. Positive alongtrack_wind = tailwind, positive crosstrack_wind = wind from left
      alongtrack_wind, crosstrack_wind = wind_components(wind_speed_at_altitude, wind_direction_at_altitude, ground_track)

      # TODO: select speed to fly
      if selected_airspeed <= 0:
        airspeed = selected_glider.best_glide_at/3.6     #m/s
      else:
        airspeed = selected_airspeed/3.6                 #m/s

      # add x % of headwind
      if alongtrack_wind < 0:       # headwind
        airspeed += headwind_correction*abs(alongtrack_wind)

      if vertical_airmass_velocity < 0:
        airspeed += -1*vertical_airmass_velocity*AS_due_VV_correction/3.6

     # calculate vertical velocity    
      total_VV = vertical_airmass_velocity - selected_glider.sinkAtAirspeed(airspeed*3.6)

      # GS calculation
      if airspeed**2 - crosstrack_wind**2 < 0:
        GS = 0
      else:
        GS = alongtrack_wind + math.sqrt(airspeed**2 - crosstrack_wind**2)

      # x_vel and y_vel calculation
      x_vel, y_vel = polarToCartesian(GS, ground_track)

      # integration
      altitude += total_VV*dT
      x_pos -= x_vel*dT         # from the limit of glide range towards airfied ==> minus sign
      y_pos -= y_vel*dT         # from the limit of glide range towards airfied ==> minus sign
      time += dT

      # Geometric glide ratio calculation
      LperD = -GS/total_VV
  
      time_list.append(time)
      airspeed_list.append(airspeed*3.6)
      groundspeed_list.append(GS*3.6)
      vv_list.append(total_VV)
      altitude_list.append(altitude)
      LperD_list.append(LperD)


    # save this track LAR data to dict
    glide_LAR[ground_track] = [x_pos, y_pos, time]
    X_pos_list.append(x_pos/1000)
    y_pos_list.append(y_pos/1000)
    glide_values[ground_track] = [time_list, airspeed_list, groundspeed_list, vv_list, altitude_list, LperD_list]

  X_pos_list.append(X_pos_list[0])    #close LAR circle
  y_pos_list.append(y_pos_list[0])    #close LAR circle

  max_range_HDG, min_range_HDG = max_min_range_heading(glide_LAR)   # Find direction of maximum and minimum range

  LAR_figure_ax = plotAirfielCenteredLAR(graph_color, LAR_figure_ax, glide_LAR, X_pos_list, y_pos_list, max_range_HDG, min_range_HDG)

  desired_track_HDG = min_range_HDG
  desired_track_figure_ax = plotDesiredTrackValues(graph_color, desired_track_figure_ax, glide_values[desired_track_HDG], desired_track_HDG)

  # -------------------------- END OF AIRFIELD CENTERED GLIDER RANGE ----------------------------

plt.show()  # Show lar figure
# Save the plot as a PNG file
LAR_figure.savefig('results/drag_polars.png')

# ----------------------------------- END OF SCENRIOS --------------------------------------------


# -------------------------------------- MAP PLOTTER ------------------------------------------
# TODO: plot multiple scanarios on map
# Create the map plotter:
apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(*airfield_location, 14, apikey=apikey, map_type='satellite')

# Outline the EFJM_RWY0927:
EFJM_RWY0927 = zip(*[
    (61.781701, 22.701878),
    (61.781545, 22.701854),
    (61.780998, 22.718288),
    (61.781125, 22.718308)
])
gmap.polygon(*EFJM_RWY0927 , color='cornflowerblue', edge_width=1)

# Mark EFJM:
gmap.marker(*EFJM, color='w', title='EFJM')
# Mark EFPI:
gmap.marker(*EFPI, color='w', title='EFPI')

# LAR drawing:
LAT_list = []
LON_list = []
for track_HDG in glide_LAR:
  # print(ground_track)
  LAT, LON = relativePosToCoordinates(*airfield_location, glide_LAR[track_HDG][0], glide_LAR[track_HDG][1])
  LAT_list.append(LAT)
  LON_list.append(LON)
LAT, LON = relativePosToCoordinates(*airfield_location, glide_LAR[0][0], glide_LAR[0][1])
LAT_list.append(LAT)
LON_list.append(LON)
# Plot the polygon without fill
gmap.plot(LAT_list, LON_list, color=hex_color , edge_width=2)

#draw min ditance line
min_distance_point = relativePosToCoordinates(*airfield_location, glide_LAR[min_range_HDG][0], glide_LAR[min_range_HDG][1])
gmap.plot([airfield_location[0], min_distance_point[0]],
          [airfield_location[1], min_distance_point[1]], color=hex_color, edge_width=2)
gmap.marker(*min_distance_point, title='Min distance {:.1f} km, HDG {:.0f} degT'.format(math.sqrt(glide_LAR[min_range_HDG][0]**2 + glide_LAR[min_range_HDG][1]**2)/1000, min_range_HDG), color=hex_color)

# WIND ARROWS
# wind arrow offset from airfield
offset = 1500   #m
arrow_scale = 1000  #km / 10m/s
start_lat, start_lon = relativePosToCoordinates(*airfield_location, offset, offset)
# Draw SFC wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[0], winds_speeds[0], arrow_scale, name="SFC", color="r")
# Draw 500m wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[1], winds_speeds[1], arrow_scale, name="500m", color="w")
# Draw 1000m wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[2], winds_speeds[2], arrow_scale, name="1 km", color="m")
# Draw 2000m wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[3], winds_speeds[3], arrow_scale, name="2 km", color="y")


# Draw the map:
gmap.draw('results/map.html')

# --------------------------------- END OF MAP PLOTTER ----------------------------------------



# ------------------------- OPTIMAL FLIGHT TO GIVEN TRACK DIRECTION ---------------------------

number = 0  # optimum flight calculation for fist scenario
selected_glider = gliders_dict[scenarios[number].glider_file]
track_HDG = 0

vv_airmass_list = np.linspace(0,-2, 50)
airspeed_list = np.linspace(70, 180, 500)       #km/h

# Initialize figure
figure_1, figure_1_ax = plt.subplots()

best_GR_AS_VV_list = []

for vv_airmass in vv_airmass_list:
  glide_ratio_list = []
  best_GR = 0
  best_speed = 0
  best_total_VV = 0

  for airspeed in airspeed_list:

    # calculate vertical velocity    
    total_VV = vv_airmass - selected_glider.sinkAtAirspeed(airspeed)

    # Ground speed calculation
    GS = airspeed

    # Geometric glide ratio calculation
    GR = -GS/3.6/total_VV

    if GR > best_GR:
      best_GR = GR
      best_speed = airspeed
      best_total_VV = total_VV

    glide_ratio_list.append(GR)

  best_GR_AS_VV_list.append([vv_airmass, best_GR, best_speed, best_total_VV])

  legend = "VV = {:.1f} m/s".format(vv_airmass)
  figure_1_ax = plotPoints(figure_1_ax, airspeed_list, glide_ratio_list, "AS (km/h)", "GR", legend)

best_VV = []
best_GR = []
best_AS = []
best_VV_tot = []
for list in best_GR_AS_VV_list:
  best_VV.append(list[0])
  best_GR.append(list[1])
  best_AS.append(list[2])
  best_VV_tot.append(list[3])

figure_1_ax = plotPoints(figure_1_ax, best_AS, best_GR, "AS (km/h)", "GR", "max")

# Initialize figure
figure_2, figure2_ax = plt.subplots(1,3)
figure2_ax = plotOptimalFlightValues(figure2_ax, best_AS, best_VV, best_GR, best_VV_tot)

plt.show()  # Show lar figure
# Save the plot as a PNG file
figure_1.savefig('results/optimum_flight_values.png')
figure_2.savefig('results/optimum_speed_vs_VV.png')


# -------------------- END OF  OPTIMAL FLIGHT TO GIVEN TRACK DIRECTION ------------------------

# webbrowser.open('http://ennuste.ilmailuliitto.fi/0/sounding10.curr.1000lst.d2.png')
# webbrowser.open('map.html')


print("SIMULATION COMPLETE")

