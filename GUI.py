import tkinter as tk
from tkinter import filedialog

from scenario import Scenario

def GUI(scenarios):
  
    def on_wind_unit_select(event):
        selected_wind_unit.set(selected_wind_unit.get())  # Update the label with the selected option

    def read_input_data():
        ID = str(ID_entry.get())
        start_altitude = float(start_altitude_entry.get())
        end_altitude = float(end_altitude_entry.get())
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

        scenario = Scenario(ID, glider_filname, start_altitude, end_altitude, airmass_vv, winds)

        scenarios[ID] = scenario
        # ID_entry.insert(0, ID_entry.get()+'1')    #autoupdate scanario nro

    def select_file():
        filename = filedialog.askopenfilename()
        if filename:
            name = filename.split("/")[-1]
            file_label_entry.delete(0, tk.END)
            file_label_entry.insert(0, f"{name}")
            # file_label.config(text=f"Selected file: {name}")




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

    # SFC wind
    label = tk.Label(window, text="SFC wind:")
    label.grid(row=row+2, column=column+0, padx=10, pady=10)
    wind_0_direction_entry = tk.Entry(window, width=5)
    wind_0_direction_entry.insert(0, "0")        # default value
    wind_0_direction_entry.grid(row=row+2, column=column+1, padx=10, pady=10)
    wind_0_speed_entry = tk.Entry(window, width=5)
    wind_0_speed_entry.insert(0, "3")        # default value
    wind_0_speed_entry.grid(row=row+2, column=column+2, padx=10, pady=10)
    # 500m wind
    label = tk.Label(window, text="500m wind:")
    label.grid(row=row+3, column=column+0, padx=10, pady=10)
    wind_1_direction_entry = tk.Entry(window, width=5)
    wind_1_direction_entry.insert(0, "30")        # default value
    wind_1_direction_entry.grid(row=row+3, column=column+1, padx=10, pady=10)
    wind_1_speed_entry = tk.Entry(window, width=5)
    wind_1_speed_entry.insert(0, "10")        # default value
    wind_1_speed_entry.grid(row=row+3, column=column+2, padx=10, pady=10)
    # 1000m wind
    label = tk.Label(window, text="1km wind:")
    label.grid(row=row+4, column=column+0, padx=10, pady=10)
    wind_2_direction_entry = tk.Entry(window, width=5)
    wind_2_direction_entry.insert(0, "60")        # default value
    wind_2_direction_entry.grid(row=row+4, column=column+1, padx=10, pady=10)
    wind_2_speed_entry = tk.Entry(window, width=5)
    wind_2_speed_entry.insert(0, "12")        # default value
    wind_2_speed_entry.grid(row=row+4, column=column+2, padx=10, pady=10)
    # 2000m wind
    label = tk.Label(window, text="2km wind:")
    label.grid(row=row+5, column=column+0, padx=10, pady=10)
    wind_3_direction_entry = tk.Entry(window, width=5)
    wind_3_direction_entry.insert(0, "90")        # default value
    wind_3_direction_entry.grid(row=row+5, column=column+1, padx=10, pady=10)
    wind_3_speed_entry = tk.Entry(window, width=5)
    wind_3_speed_entry.insert(0, "15")        # default value
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
