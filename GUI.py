import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser

from scenario import Scenario
from functions import rgb_to_hex

def show_parameters(objects):
    popup = tk.Toplevel()
    popup.title("Scenario parameters")

    text_widget = tk.Text(popup, wrap="word", width=100, height=50)
    text_widget.pack(padx=10, pady=10)


    for i, (key, obj) in enumerate(objects.items()):
        text_widget.insert(tk.END, f"Scenario: {key}\n")
        graph_color = obj.color
        color = rgb_to_hex(graph_color)
        tag_name = f"color_{i}"  # Create a unique tag name for each object
        text_widget.tag_configure(tag_name, foreground=color)  # Define the tag with custom color

        for attr, value in vars(obj).items():
            text_widget.insert(tk.END, f"{attr}: {value}\n", tag_name)  # Apply the tag to set the text color
        text_widget.insert(tk.END, "\n")

def GUI(scenarios):

    def show_scenarios():
        show_parameters(scenarios)

    def read_input_data():
        if len(scenarios) == 0:
            scenario_number = 0
        else:
            # Get the last key-value pair from the dictionary
            last_key = list(scenarios.keys())[-1]
            scenario_number = last_key + 1

        ID = str(ID_entry.get())

        color = str(selected_color_entry.get())
        # Convert text representation to a tuple using eval() function
        rgb_color_tuple = eval(color)
        # Convert RGB values to values between 0 and 1
        graph_color = (rgb_color_tuple[0] / 255, rgb_color_tuple[1] / 255, rgb_color_tuple[2] / 255)

        start_altitude = float(start_altitude_entry.get())
        end_altitude = float(end_altitude_entry.get())
        airspeed = float(airspeed_entry.get())
        headwind_correction = float(headwind_correction_entry.get())
        AS_VV_correction = float(AS_VV_correction_entry.get())
        airmass_vv = float(airmass_vv_entry.get())
        glider_filname = file_label_entry.get()
        w0s = float(wind_0_speed_entry.get())
        w1s = float(wind_1_speed_entry.get())
        w2s = float(wind_2_speed_entry.get())
        w3s = float(wind_3_speed_entry.get())
        w0d = float(wind_0_direction_entry.get())
        w1d = float(wind_1_direction_entry.get())
        w2d = float(wind_2_direction_entry.get())
        w3d = float(wind_3_direction_entry.get())
        wind_unit = selected_wind_unit.get()
        if wind_unit == "m/s":
            factor = 1
        if wind_unit == "kts":
            factor = 0.514444

        winds = [
            [0,        factor*w0s,     w0d],
            [500,      factor*w1s,     w1d],
            [1000,     factor*w2s,     w2d],
            [2000,     factor*w3s,     w3d]
            ]

        scenario = Scenario(scenario_number, ID, graph_color, glider_filname, start_altitude, end_altitude, airspeed, headwind_correction, AS_VV_correction, airmass_vv, winds)

        scenarios[scenario_number] = scenario

        print("Scenario name: " + str(scenario.ID) + ", number: " + str(scenario.scenario_number))

        # print(scenarios)
        # ID_entry.insert(0, ID_entry.get()+'1')    #autoupdate scanario nro

    def select_file():
        filename = filedialog.askopenfilename()
        if filename:
            name = filename.split("/")[-1]
            file_label_entry.delete(0, tk.END)
            file_label_entry.insert(0, f"{name}")
            # file_label.config(text=f"Selected file: {name}")

    def choose_color():
        color = colorchooser.askcolor(title="Choose color")
        if color[1]:  # Check if a color was selected
            selected_color_entry.config(bg=color[1])  # Set the background color of the label
            selected_color_entry.delete(0, tk.END)
            selected_color_entry.insert(0, f"{color[0]}")

    def on_wind_unit_select(event):
        selected_wind_unit.set(selected_wind_unit.get())  # Update the label with the selected option


    # Create the main window
    window = tk.Tk()
    window.title("Advanced Glide Range Simulator")

    row = 1
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

    row = 3
    column = 0  
    # Speed selaction logic
    label = tk.Label(window, text="Airspeed selection:")
    label.grid(row=row+0, column=column+0, padx=10, pady=10)
    # Speed selection logic
    label = tk.Label(window, text="Airspeed (0=best L/D):")
    label.grid(row=row+1, column=column+0, padx=10, pady=10)
    airspeed_entry = tk.Entry(window)
    airspeed_entry.insert(0, "0")        # default value
    airspeed_entry.grid(row=row+1, column=column+1, padx=10, pady=10)
    # Speed selection logic
    label = tk.Label(window, text="Headwind correction factor:")
    label.grid(row=row+2, column=column+0, padx=10, pady=10)
    headwind_correction_entry = tk.Entry(window)
    headwind_correction_entry.insert(0, "0")        # default value
    headwind_correction_entry.grid(row=row+2, column=column+1, padx=10, pady=10)
    # Speed selection logic
    label = tk.Label(window, text="AS increase due VV (km/h / m/s):")
    label.grid(row=row+3, column=column+0, padx=10, pady=10)
    AS_VV_correction_entry = tk.Entry(window)
    AS_VV_correction_entry.insert(0, "0")        # default value
    AS_VV_correction_entry.grid(row=row+3, column=column+1, padx=10, pady=10)

    row = -1
    column = 3
    # wind units
    label = tk.Label(window, text="(degT):")
    label.grid(row=row+1, column=column+1, padx=10, pady=10)
    # Options for the dropdown menu
    options = ["m/s", "kts"]
    # Variable to store the selected option
    selected_wind_unit = tk.StringVar(window)
    selected_wind_unit.set(options[0])
    # Set default value for selected_option
    wind_unit_select = tk.OptionMenu(window, selected_wind_unit, *options, command=on_wind_unit_select)
    wind_unit_select.grid(row=row+1, column=column+2, padx=10, pady=10)

    default_direction = 0
    default_speed = 0
    # SFC wind
    label = tk.Label(window, text="SFC wind:")
    label.grid(row=row+2, column=column+0, padx=10, pady=10)
    wind_0_direction_entry = tk.Entry(window, width=5)
    wind_0_direction_entry.insert(0, default_direction)        # default value
    wind_0_direction_entry.grid(row=row+2, column=column+1, padx=10, pady=10)
    wind_0_speed_entry = tk.Entry(window, width=5)
    wind_0_speed_entry.insert(0, default_speed)        # default value
    wind_0_speed_entry.grid(row=row+2, column=column+2, padx=10, pady=10)
    # 500m wind
    label = tk.Label(window, text="500m wind:")
    label.grid(row=row+3, column=column+0, padx=10, pady=10)
    wind_1_direction_entry = tk.Entry(window, width=5)
    wind_1_direction_entry.insert(0, default_direction)        # default value
    wind_1_direction_entry.grid(row=row+3, column=column+1, padx=10, pady=10)
    wind_1_speed_entry = tk.Entry(window, width=5)
    wind_1_speed_entry.insert(0, default_speed)        # default value
    wind_1_speed_entry.grid(row=row+3, column=column+2, padx=10, pady=10)
    # 1000m wind
    label = tk.Label(window, text="1km wind:")
    label.grid(row=row+4, column=column+0, padx=10, pady=10)
    wind_2_direction_entry = tk.Entry(window, width=5)
    wind_2_direction_entry.insert(0, default_direction)        # default value
    wind_2_direction_entry.grid(row=row+4, column=column+1, padx=10, pady=10)
    wind_2_speed_entry = tk.Entry(window, width=5)
    wind_2_speed_entry.insert(0, default_speed)        # default value
    wind_2_speed_entry.grid(row=row+4, column=column+2, padx=10, pady=10)
    # 2000m wind
    label = tk.Label(window, text="2km wind:")
    label.grid(row=row+5, column=column+0, padx=10, pady=10)
    wind_3_direction_entry = tk.Entry(window, width=5)
    wind_3_direction_entry.insert(0, default_direction)        # default value
    wind_3_direction_entry.grid(row=row+5, column=column+1, padx=10, pady=10)
    wind_3_speed_entry = tk.Entry(window, width=5)
    wind_3_speed_entry.insert(0, default_speed)        # default value
    wind_3_speed_entry.grid(row=row+5, column=column+2, padx=10, pady=10)
    # Airmass vertical velocity
    label = tk.Label(window, text="Airmass VV:")
    label.grid(row=row+6, column=column+0, padx=10, pady=10)
    airmass_vv_entry = tk.Entry(window, width=5)
    airmass_vv_entry.insert(0, "0")        # default value
    airmass_vv_entry.grid(row=row+6, column=column+2, padx=10, pady=10)

    row = 10
    column = 0
    # Scenario ID
    label = tk.Label(window, text="Scenario ID:")
    label.grid(row=row+0, column=column+0, padx=10, pady=10)
    ID_entry= tk.Entry(window)
    #ID_entry.insert(0, "")        # default value
    ID_entry.grid(row=row+0, column=column+1, padx=10, pady=10)

    # Create a button to open the file explorer
    file_button = tk.Button(window, text="Select glider file", command=select_file)
    file_button.grid(row=9, column=0, padx=10, pady=10)

    # Label to display the selected file
    # file_label = tk.Label(window, text="")
    # file_label.grid(row=9, column=1, padx=10, pady=10)
    file_label_entry = tk.Entry(window)
    file_label_entry.grid(row=9, column=1, padx=10, pady=10)

    # Create a button to open the color chooser
    choose_color_button = tk.Button(window, text="Choose Color", command=choose_color)
    choose_color_button.grid(row=10, column=0, padx=10, pady=10)
    # Create a label to display the selected color
    selected_color_entry = tk.Entry(window)
    selected_color_entry.grid(row=10, column=1, padx=10, pady=10)

    # Create scenario
    create_scenario_button = tk.Button(window, text="Create scenario", command=read_input_data)
    create_scenario_button.grid(row=11, column=1, padx=10, pady=10)

    # Show scenario
    show_scenarios_button = tk.Button(window, text="Show scenarios", command=show_scenarios)
    show_scenarios_button.grid(row=11, column=2, padx=10, pady=10)

    # Run the main event loop
    window.mainloop()
