# Import libraries
import gmplot
import numpy
import webbrowser
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import filedialog

# Import Classes and functions
from Glider import Glider
from scenario import Scenario
from functions import relativePosToCoordinates
from functions import polarToCartesian
from functions import read_points_from_csv
from functions import plotDragPolars
from functions import plotAirfielCenteredLAR
from functions import printLogo
from functions import wind_components
from functions import draw_arrow


printLogo()

# ------------------------------------------ POINTS ------------------------------------------

EFJM = (61.781338, 22.710170)
EFPI = (61.245626, 22.193343)

# -------------------------------------- END OF POINTS ----------------------------------------

# ---------------------------------- CREATE SCENARIO DICT -------------------------------------
global scenarios
scenarios = {}
# ------------------------------ END OF CREATE SCENARIO DICT ----------------------------------

# --------------------------------------- GUI -------------------------------------------------

# Create the main window
window = tk.Tk()
window.title("Advanced Glide Range Simulator")


def read_input_data():
  ID = str(ID_entry.get())
  start_altitude = float(start_altitude_entry.get())
  end_altitude = float(end_altitude_entry.get())
  airmass_vv = float(airmass_vv_entry.get())
  glider_filname = file_label_entry.get()

  scenario = Scenario(ID, glider_filname, start_altitude, end_altitude, airmass_vv)

  scenarios[ID] = scenario
  # ID_entry.insert(0, ID_entry.get()+'1')    #autoupdate scanario nro

  print(scenarios)

def select_file():
  filename = filedialog.askopenfilename()
  if filename:
    name = filename.split("/")[-1]
    file_label_entry.delete(0, tk.END)
    file_label_entry.insert(0, f"{name}")
    # file_label.config(text=f"Selected file: {name}")

row = 2
column = 0  
# Start altitude
label = tk.Label(window, text="Start altitude (m ASL):")
label.grid(row=row+0, column=column+0, padx=10, pady=10)
start_altitude_entry = tk.Entry(window)
start_altitude_entry.insert(0, "1000")        # default value
start_altitude_entry.grid(row=row+0, column=column+1, padx=10, pady=10)
# End altitude
label = tk.Label(window, text="End altitude (m ASL):")
label.grid(row=row+1, column=column+0, padx=10, pady=10)
end_altitude_entry = tk.Entry(window)
end_altitude_entry.insert(0, "300")        # default value
end_altitude_entry.grid(row=row+1, column=column+1, padx=10, pady=10)

row = 5
column = 0
# Airmass vertical velocity
label = tk.Label(window, text="Airmass VV (m/s):")
label.grid(row=row+1, column=column+0, padx=10, pady=10)
airmass_vv_entry = tk.Entry(window)
airmass_vv_entry.insert(0, "0")        # default value
airmass_vv_entry.grid(row=row+1, column=column+1, padx=10, pady=10)

row = 10
column = 0
# Scenario ID
label = tk.Label(window, text="Scenario ID:")
label.grid(row=row+0, column=column+0, padx=10, pady=10)
ID_entry= tk.Entry(window)
ID_entry.insert(0, "0")        # default value
ID_entry.grid(row=row+0, column=column+1, padx=10, pady=10)

# Create a button to open the file explorer
file_button = tk.Button(window, text="Select glider file", command=select_file)
file_button.grid(row=9, column=0, padx=10, pady=10)

# Label to display the selected file
# file_label = tk.Label(window, text="")
# file_label.grid(row=9, column=1, padx=10, pady=10)
file_label_entry = tk.Entry(window)
file_label_entry.grid(row=9, column=1, padx=10, pady=10)

# Create scenario
calculate_button = tk.Button(window, text="Create scenario", command=read_input_data)
calculate_button.grid(row=10, column=3, padx=10, pady=10)

# Run the main event loop
window.mainloop()


# ------------------------------------ END OF GUI --------------------------------------------

# ------------------------------------- CREATING GLIDER ---------------------------------------

#select gliders
# glider_filenames = ["gliders/ASK21_570kg.csv", 
#                     #"gliders/ASK21_470kg.csv",
#                     "gliders/ASK23_346kg.csv",
#                     "gliders/ASTIR_CS_JEANS_350kg.csv"]

glider_filenames = []
for ID in scenarios:
  glider_filenames.append(scenarios[ID].glider_file)

print(glider_filenames)

# Create a Dict of gliders
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

  # print("Glider ", i, " name: ", glider.name)

  gliders_dict[file_name] = glider        #use filename as key

plotDragPolars(gliders_dict)

# -------------------------------- END OF CREATING GLIDER -------------------------------------

LAR_figure, LAR_figure_ax = plt.subplots()  # Create LAR figure

for ID in scenarios:

  # ---------------------------------- SCENARIO PARAMETERS --------------------------------------

  # TODO: manage scenarios with csv file
  print(gliders_dict.keys())
  selected_glider = gliders_dict[scenarios[ID].glider_file]
  airfield_location = EFJM
  end_altitude = scenarios[ID].end_altitude
  start_altitude = scenarios[ID].start_altitude
  dT = 1                        #s

  vertical_airmass_velocity = scenarios[ID].airmass_vv
  # Winds [(altitude_meters, speed_m/s, direction_degrees_TRUE)]
  winds = [
      [0,         5,      70],
      [1000,      10,     60],
      [2000,      15,     20],
      [3000,      20,     0]
      ]

  # TODO: selected airspeed logic

  print('SELECTED GLIDER:')
  print('Name: ', selected_glider.name)
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


  # Simulation

  glide_LAR = {}
  X_pos_list = []
  y_pos_list = []

  for track_heading in range(0, 359, 10):

    altitude = start_altitude
    time = 0
    x_pos = 0
    y_pos = 0

    #simulation of flight to heading
    while altitude > end_altitude:

      # linear interpolation
      wind_speed_at_altitude = numpy.interp(altitude, winds_altitudes, winds_speeds,
                                            left=None, right=None, period=None)
      wind_direction_at_altitude = numpy.interp(altitude, winds_altitudes, winds_directions,
                                            left=None, right=None, period=None)
      
      # TODO: select speed to fly
      airspeed = selected_glider.best_glide_at/3.6     #m/s

      # calculate vertical velocity
      total_VV = vertical_airmass_velocity - selected_glider.sinkAtAirspeed(airspeed)

      # calculate wind components. Positive alongtrack_wind = tailwind, positive crosstrack_wind = wind from left
      alongtrack_wind, crosstrack_wind = wind_components(wind_speed_at_altitude, wind_direction_at_altitude, track_heading)

      # GS calculation
      GS = alongtrack_wind + math.sqrt(airspeed**2 - crosstrack_wind**2)

      # x_vel and y_vel calculation
      x_vel, y_vel = polarToCartesian(GS, track_heading)

      # integration
      altitude += total_VV*dT
      x_pos -= x_vel*dT         # from the limit of glide range towards airfied ==> minus sign
      y_pos -= y_vel*dT         # from the limit of glide range towards airfied ==> minus sign
      time += dT

    # save this track LAR data to dict
    glide_LAR[track_heading] = [x_pos, y_pos, time]
    X_pos_list.append(x_pos/1000)
    y_pos_list.append(y_pos/1000)

  X_pos_list.append(X_pos_list[0])    #close LAR circle
  y_pos_list.append(y_pos_list[0])    #close LAR circle

  min_range = 9999999999
  min_range_HDG = 0
  max_range_HDG = 0
  max_range = 0

  for HDG in glide_LAR:
    r = math.sqrt(glide_LAR[HDG][0]**2 + glide_LAR[HDG][1]**2)
    if r > max_range:
      max_range = r
      max_range_HDG = HDG
    if r < min_range:
      min_range = r
      min_range_HDG = HDG

  LAR_figure_ax = plotAirfielCenteredLAR(LAR_figure_ax, glide_LAR, X_pos_list, y_pos_list, max_range_HDG, min_range_HDG)

  # -------------------------- END OF AIRFIELD CENTERED GLIDER RANGE ----------------------------

plt.show()
# Save the plot as a PNG file
# LAR_figure.savefig('results/drag_polars.png')

# -------------------------------------- MAP PLOTTER ------------------------------------------
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
  # print(track_heading)
  LAT, LON = relativePosToCoordinates(*airfield_location, glide_LAR[track_HDG][0], glide_LAR[track_HDG][1])
  LAT_list.append(LAT)
  LON_list.append(LON)
LAT, LON = relativePosToCoordinates(*airfield_location, glide_LAR[0][0], glide_LAR[0][1])
LAT_list.append(LAT)
LON_list.append(LON)
# Plot the polygon without fill
gmap.plot(LAT_list, LON_list, color='r', edge_width=2)

#draw min ditance line
min_distance_point = relativePosToCoordinates(*airfield_location, glide_LAR[min_range_HDG][0], glide_LAR[min_range_HDG][1])
gmap.plot([airfield_location[0], min_distance_point[0]],
          [airfield_location[1], min_distance_point[1]], color='r', edge_width=2)
gmap.marker(*min_distance_point, title='Min distance {:.1f} km, HDG {:.0f} degT'.format(math.sqrt(glide_LAR[min_range_HDG][0]**2 + glide_LAR[min_range_HDG][1]**2)/1000, min_range_HDG))

# WIND ARROWS
# wind arrow offset from airfield
offset = 1500   #m
arrow_scale = 1000  #km / 10m/s
start_lat, start_lon = relativePosToCoordinates(*airfield_location, offset, offset)
# Draw SFC wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[0], winds_speeds[0], arrow_scale, name="SFC", color="r")
# Draw 1000m wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[1], winds_speeds[1], arrow_scale, name="1 km", color="w")
# Draw 2000m wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[2], winds_speeds[2], arrow_scale, name="2 km", color="m")
# Draw 3000m wind arrow
draw_arrow(gmap, start_lat, start_lon, winds_directions[3], winds_speeds[3], arrow_scale, name="3 km", color="y")


# Draw the map:
gmap.draw('results/map.html')

# --------------------------------- END OF MAP PLOTTER ----------------------------------------

# webbrowser.open('http://ennuste.ilmailuliitto.fi/0/sounding10.curr.1000lst.d2.png')
# webbrowser.open('map.html')

print("SIMULATION COMPLETE")

