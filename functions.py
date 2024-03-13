from geopy.distance import distance
from geopy.point import Point
import math
import csv
import matplotlib.pyplot as plt
import gmplot

def printLogo():
    print("    _       _                               _    ____ _ _     _              ")
    print("   / \   __| |_   ____ _ _ __   ___ ___  __| |  / ___| (_) __| | ___         ")
    print("  / _ \ / _` \ \ / / _` | '_ \ / __/ _ \/ _` | | |  _| | |/ _` |/ _ \        ")
    print(" / ___ \ (_| |\ V / (_| | | | | (_|  __/ (_| | | |_| | | | (_| |  __/        ")
    print("/_/__ \_\__,_| \_/ \__,_|_| |_|\___\___|\__,_|  \____|_|_|\__,_|\___|        ")
    print("|  _ \ __ _ _ __   __ _  ___  / ___|(_)_ __ ___  _   _| | __ _| |_ ___  _ __ ")
    print("| |_) / _` | '_ \ / _` |/ _ \ \___ \| | '_ ` _ \| | | | |/ _` | __/ _ \| '__|")
    print("|  _ < (_| | | | | (_| |  __/  ___) | | | | | | | |_| | | (_| | || (_) | |   ")
    print("|_| \_\__,_|_| |_|\__, |\___| |____/|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|   ")
    print("                  |___/                                                      ")
    
def relativePosToCoordinates(origin_LAT, origin_LON, x_meters, y_meters):
    """
    Calculate the latitude and longitude coordinates relative to a given origin
    based on a relative distance in meters.

    Args:
        origin_LAT (float): Latitude of the origin point.
        origin_LON (float): Longitude of the origin point.
        x_meters (float): Relative distance in meters along the longitude axis.
        y_meters (float): Relative distance in meters along the latitude axis.

    Returns:
        tuple: Latitude and longitude coordinates relative to the origin.
    """
  # Create a Point object for the origin
    origin_point = Point(origin_LAT, origin_LON)

    # Calculate the destination point based on the relative distances
    destination_point = distance(meters=y_meters).destination(origin_point, 0)
    destination_point = distance(meters=x_meters).destination(destination_point, 90)

    return destination_point.latitude, destination_point.longitude

def polarToCartesian(radius, angle_degrees):
    """
    Convert polar coordinates to Cartesian coordinates.

    Args:
        radius (float): The distance from the origin (r).
        angle_degrees (float): The angle in degrees.

    Returns:
        tuple: Cartesian coordinates (x, y).
    """
    # origin to north, clockwise positive direction
    angle_degrees = -angle_degrees
    angle_degrees += 90

    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)

    # Calculate Cartesian coordinates
    x = radius * math.cos(angle_radians)
    y = radius * math.sin(angle_radians)

    return x, y

def wind_components(wind_speed, wind_direction, track_HDG):
    # Convert wind_direction and aircraft_HDG to radians
    wind_direction_rad = math.radians(wind_direction+180)
    aircraft_HDG_rad = math.radians(track_HDG)
    
    # Calculate wind components
    alongtrack = wind_speed * math.cos(wind_direction_rad - aircraft_HDG_rad)
    crosstrack = wind_speed * math.sin(wind_direction_rad - aircraft_HDG_rad)
    
    return alongtrack, crosstrack

def max_min_range_heading(glide_LAR):
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

    return max_range_HDG, min_range_HDG

def read_points_from_csv(csv_file):
    """

    """
    points = []
    data = {}
    dragpolar_data = False

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            if len(row) == 2:  # Ensure there are exactly two elements in the row
                parameter_name, value = row
                if not parameter_name.startswith('#'):  # Ignore lines starting with #
                    if parameter_name == "airspeed (km/h)":
                        dragpolar_data = True
                    elif dragpolar_data:
                        points.append([float(row[0]), float(row[1])])
                    else:    
                        data[parameter_name.strip()] = value.strip()  # Strip whitespace from parameter_name and value

    return data, points

def plotPoints(x_points, y_points,x_label, y_label):
    """
    Plot x, y points.

    Args:
        x_points (list): List of x coordinates.
        y_points (list): List of y coordinates.
    """
    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.plot(x_points, y_points, color='blue')  # Plot points as circles
    plt.title('X-Y Points Plot')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()

def plotDragPolars(gliders):
    """
    Plot drag polars of input glider list.

    Args:
        Dictonary of gliders.
    """
    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    for name in gliders:
        plt.plot(gliders[name].drag_polar_AS, gliders[name].drag_polar_VV, label=gliders[name].name)  # Plot points as circles
    plt.title('Drag polar')
    plt.xlabel('Airspeed (km/h)')
    plt.ylabel('Sink rate (m/s)')
    plt.legend(loc='upper right')
    plt.ylim(0, 4)
    plt.gca().invert_yaxis()
    plt.grid(True)
    # Save the plot as a PNG file
    plt.savefig('results/drag_polars.png')
    plt.show()

def plotAirfielCenteredLAR(ax, LAR, x, y, max_range_HDG, min_range_HDG):
    """
    Plot Airfield centered LAR.

    Args:
        
    """
    # plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    ax.plot(0, 0, "o")
    ax.plot(x, y, "r")  # 
    ax.plot([0, LAR[max_range_HDG][0]/1000], [0, LAR[max_range_HDG][1]/1000], "r--", label=str("max: "+"{:.1f}".format(math.sqrt(LAR[max_range_HDG][0]**2 + LAR[max_range_HDG][1]**2)/1000)+" km"))
    ax.plot([0, LAR[min_range_HDG][0]/1000], [0, LAR[min_range_HDG][1]/1000], "r-.", label=str("max: "+"{:.1f}".format(math.sqrt(LAR[min_range_HDG][0]**2 + LAR[min_range_HDG][1]**2)/1000)+" km"))
    ax.set_title('Airfield centered glide range')
    ax.set_xlabel('(km)')
    ax.set_ylabel('(km)')
    ax.legend(loc='upper right')
    ax.grid(True)
    ax.axis('equal')
    
    
    return ax

def draw_arrow(gmap, start_lat, start_lon, direction, wind_speed, radius, name, color='red'):
    radius = wind_speed/10*radius
    arrow_width = 0.1*radius
    end_lat, end_lon = relativePosToCoordinates(start_lat, start_lon, *polarToCartesian(radius, direction + 180))
    mid_lat = (start_lat + end_lat)/2
    mid_lon = (start_lon + end_lon)/2
    left_lat, left_lon = relativePosToCoordinates(mid_lat, mid_lon, *polarToCartesian(arrow_width, direction + 90))
    right_lat, right_lon = relativePosToCoordinates(mid_lat, mid_lon, *polarToCartesian(arrow_width, direction - 90))
    # Draw lines to simulate the arrow shaft
    gmap.plot([start_lat, end_lat], [start_lon, end_lon], color=color, edge_width=2)
    gmap.plot([left_lat, end_lat], [left_lon, end_lon], color=color, edge_width=2)
    gmap.plot([right_lat, end_lat], [right_lon, end_lon], color=color, edge_width=2)
    gmap.marker(end_lat, end_lon, color=color, title=name+" {:.0f} degT, {:.1f} m/s".format(direction, wind_speed), info_window=name+" {:.0f} degT, {:.1f} m/s".format(direction, wind_speed))
    # gmap.plot([mid_lat, end_lat], [mid_lng, end_lng], color=color, edge_width=5)
