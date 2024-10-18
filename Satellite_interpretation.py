# In[Proving consistnecy in rows and columns by terminal output of table]

import csv
from tabulate import tabulate

with open('Satellite.txt', 'r') as infile:
    reader = csv.reader(infile, delimiter=',')
    
    #Skipping some beginning info 
    for _ in range(4):
        next(reader)

    #Storing rows
    data = [row for row in reader]

#Displaying table in terminal to feature conciseness
table = tabulate(data, headers='firstrow', tablefmt='')
print(table)


# In[Saving in various forms]:
    
def filter_start_time(init_range, header=True): #Gives back a group of satellites within a specified intial starting range.
    
    #Reading the txt file
    with open('Satellite.txt', 'r') as infile:
        reader = csv.reader(infile, delimiter=',')
        
        sk_num = 5 if header else 6
        
        for _ in range(sk_num):
            next(reader)
    
        # REading in the data into a list if time is within a given range of hours of the day
        data = []
        for i, row in enumerate(reader):
            if i == 0: data.append(row); continue #Skip header row
            hour = row[5].strip()[0:3].replace(":","")
            if init_range[0] < int(hour) < init_range[1]:
                data.append(row)
                
    return data

data = filter_start_time([10,15])

def save_table(data, format, filename):
    aligned_table = tabulate(data, headers='firstrow', tablefmt=format)
    with open(filename, 'w') as outfile:
        outfile.write(aligned_table)

save_table(data, 'latex', 'Satellite_latex.txt')
save_table(data, 'github', 'Satellite_github.txt')

    
# In[Defining important functions and varibles]:

import sys
import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from daskms import xds_from_table
from astropy import units as u

def generate_marker_color_pairs(num_pairs):
    
    #Defining marker styles and colors
    markers = ['s', '^', 'o', '>', '*']
    colors = ['b', 'g', 'r', 'm', 'y', 'c']  # Added 'c' for cyan

    mca = set() #Marker Color Alpha unique set
    
    #Generating pairs
    for i in range(num_pairs):
        marker = markers[i % len(markers)]  #Cycling through markers
        color = colors[i % len(colors)]      #Cycling through colors
        mca.add((marker, color, 1)) #Adding tuple

    if (n:=len(mca)) < num_pairs:
        sys.exit(f"Basis too small for needed tuples of (m,c,a). Can only make {n} unique tuples")
        
    return mca

def spherical_to_cartesian(alt, az):
    alt = np.radians(90 - alt)  #Altitude from zenith (90 deg) to horizon (0 deg)
    az = np.radians(az)
    x = np.sin(alt) * np.cos(az)
    y = np.sin(alt) * np.sin(az)
    z = np.cos(alt)
    return x, y, z

def direction_to_degrees(direction):
    direction_map = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90, 'ESE': 112.5, 
        'SE': 135, 'SSE': 157.5, 'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 
        'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }
    return direction_map.get(direction.strip(), None)

def plot_Meerkat_direction(ax, label:bool): #Ax to plot

    lat = -30.711056  # degrees
    lon = 21.443889   # degrees

    #Latitude and Longitude to altitude and azimuth for the spherical coordinates
    altitude = 90 - np.abs(lat)  #From lat to alt
    azimuth = lon  #longitude is treated as azimuth

    #Calculating and recording Cartesian coordinates
    x, y, z = spherical_to_cartesian(altitude, azimuth)

    #Scaling by an arbitrary distance as a rough approximation
    x *= distance_from_earth
    y *= distance_from_earth
    z *= distance_from_earth

    label = 'Phase Center'+r'$\sim(\theta, \phi)\cong (-31^\circ, 21^\circ$)' if label else ""
    
    #Plotting line from origin to "distance_from_earth" away from origin
    ax.plot([0, x], [0, y], [0, z], color='k', linestyle='--', label=label)


def interpolate_path(alt1, az1, alt2, az2, num_points=500):
    #Interpolating between two spherical coordinates along the sphere.
    
    # Interpolate altitudes and azimuths
    altitudes = np.linspace(alt1, alt2, num_points)
    azimuths = np.linspace(az1, az2, num_points)

    #Converting all alt, az paths to Cartesian pathlines
    path_coords = np.array([spherical_to_cartesian(alt, az) for alt, az in zip(altitudes, azimuths)])
    
    return path_coords

data_path = '/home/amani/Documents/HONOURS_UCT/Second_Semster/Observational_Techniques_2/OT2_Interferometry/'
ms_file = data_path + "1548939342.ms"

observation_table = xds_from_table(ms_file + "::OBSERVATION")
observation_table = dict(observation_table[0])
obs_start, obs_end = observation_table["TIME_RANGE"].compute().to_numpy()[0] * u.s

distance_from_earth = 5e2  # 500 km (rough estimation)

# In[Plotting satellites (Making Video for each 10 satellites]:

NUM = 10  # Number of satellites per video (reduces cluttering)
minimum_satellite_index = 0

colors = ['red', 'blue', 'green', 'orange', 'purple', 
          'yellow', 'pink', 'cyan', 'magenta', 'brown']
alpha = lambda: round(np.random.uniform(.3,.6), 3)
MCA = generate_marker_color_pairs(NUM)


def process_satellites_for_video(start_index, end_index, video_num):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    meerkat_legend = True

    for i in range(start_index, end_index):
        satellite = satellites[i]
        name = satellite[0].strip()

        # Start coordinates
        alt_start = float(satellite[3].replace('°', ''))
        az_start = direction_to_degrees(satellite[2].strip())

        # Peak coordinates
        alt_peak = float(satellite[7].replace('°', ''))
        az_peak = direction_to_degrees(satellite[6].strip())

        # End coordinates
        alt_end = float(satellite[11].replace('°', ''))
        az_end = direction_to_degrees(satellite[10].strip())

        if None in [az_start, az_peak, az_end]:
            print(f"Warning: Invalid direction for {name}. Skipping.")
            continue

        #converting to Cartesian coordinates
        start_coords = np.array(spherical_to_cartesian(alt_start, az_start)) * distance_from_earth
        peak_coords = np.array(spherical_to_cartesian(alt_peak, az_peak)) * distance_from_earth
        end_coords = np.array(spherical_to_cartesian(alt_end, az_end)) * distance_from_earth

        #interpolation to smooth paths
        path_start_peak = interpolate_path(alt_start, az_start, alt_peak, az_peak) * distance_from_earth
        path_peak_end = interpolate_path(alt_peak, az_peak, alt_end, az_end) * distance_from_earth

        #giving custom markers and colors to each path and end points
        marker, color, alpha = list(MCA)[i % NUM]
        random_color = random.choice(colors)

        plot_Meerkat_direction(ax, meerkat_legend)

        #Plotting paths and points
        msize = 16
        ax.scatter(path_start_peak[:, 0], path_start_peak[:, 1], path_start_peak[:, 2], 
                   color=random_color, marker='.', alpha=0.6, s=1)
        ax.scatter(path_peak_end[:, 0], path_peak_end[:, 1], path_peak_end[:, 2], 
                   color=random_color, marker='.', alpha=0.6, s=1)
        ax.scatter(*start_coords, color=color, label=f'{name}', marker=marker, s=msize, zorder=1e2)
        ax.scatter(*peak_coords, color=color, marker=marker, s=msize, zorder=1e2)
        ax.scatter(*end_coords, color=color, marker=marker, s=msize, zorder=1e2)

        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')

        meerkat_legend = False  #Showing legend only for the first satellite
        
    def update(frame):
        ax.view_init(elev=20, azim=frame)
        ax.legend(fontsize="large", loc="upper center", framealpha=0, ncol=3)
    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 1), interval=100)
    video_filename = f'satellite_trajectories_{video_num}.mp4'
    ani.save(video_filename, writer='ffmpeg', fps=30)

    plt.tight_layout()
    plt.close(fig)  #Closing the figure to free memory

satellites = filter_start_time([10,15], #in hours of the day
                               header=False)

#Generating Videos in chunks of 10 satellites if needbe (avoiding cluttering)
num_videos = (len(satellites) + NUM - 1) // NUM  # Calculating Number of videos needed

for video_num in range(num_videos):
    start_index = video_num * NUM
    end_index = min(start_index + NUM, len(satellites))  # Handle last chunk
    process_satellites_for_video(start_index, end_index, video_num + 1)