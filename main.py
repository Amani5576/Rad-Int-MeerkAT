#S. Amani Njoroge
##NJRSAM003

from scipy.optimize import curve_fit
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u, constants as c

from PACK import (ds, antenna_table,  channel_width,
                  spectral_window_table as spectral_table,
                  observation_table as obs_table, nchannels,
                  frequencies, channel_width)

from PACK_func import (argmax_more, argmin_more, 
                       plot_visibility_data, progressive_rfi_filter, 
                       plotting_hists)

# =============================================================================
# STARTER KIT
# =============================================================================

vis = ds["DATA"]
antenna_table['POSITION']
for key in obs_table.keys():
    print(f'{key}: {obs_table[key].values}')


A1 = ds["ANTENNA1"]
A2 = ds["ANTENNA2"]
ant_list = list(set(np.append(A1,A2)))
nants = len(ant_list)
inter = ds["INTERVAL"]
print(f'Total number of antennas used {nants}')
print('Interval Table Shape: ',inter.shape)
print(f'Dump rate is {np.median(inter)} s');

summary = {
    'Frequencies': frequencies,
    'No_Channeles': nchannels,
    'Channel_Width': channel_width,
    }

print(f"Frequency range (MHz): {summary['Frequencies'].min()/1.e6} - {summary['Frequencies'].max()/1.e6}")  
print(f"Total no of channles {summary['No_Channeles']}")
print(f"Channel width (kHz): {channel_width/1.e3}")

U, V, W = ds['UVW'][:,0],ds['UVW'][:,1],ds['UVW'][:,2]
plt.plot(U,V,'.')
plt.xlabel('u')
plt.ylabel('v')
plt.show()

#Below plot proves that there is a dish at the origin
plt.plot(U,V,'.')
plt.xlabel('u')
plt.ylabel('v')
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.show()

#Confirms all antenna's with 13.5 metres
print({"antenna_table['DISH_DIAMETER'].values"})

antenna_table['POSITION']
X,Y,Z = antenna_table['POSITION'][:,0],antenna_table['POSITION'][:,1],antenna_table['POSITION'][:,2]
antenna_table['POSITION']
plt.plot(X,Y, 'o')
plt.xlabel('x')
plt.ylabel('')
plt.show()

vis = ds["DATA"]
# Plotting the average across frequency slice
frequencies = spectral_table['CHAN_FREQ'].values.T
absdata = np.abs(vis[500,:,0]).compute()

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(frequencies/1e6,np.log10(absdata),'-')
ax1.set_xticks(np.arange(frequencies[0]/1.e6,frequencies[-1]/1.e6, step=100))
ax1.set_xlabel('Frequency [MHz]')
ax1.set_ylabel('Amplitude')


ax2.plot(np.log10(absdata))
ax2.set_xticks(np.arange(0,absdata.shape[0], step=128))
ax2.set_xlabel('Index no')
plt.grid()
plt.show()


# =============================================================================
# Getting all unique baselines
# =============================================================================
# Getting longest and shortest baselines in 3D
X, Y, Z = antenna_table['POSITION'][:, 0], antenna_table['POSITION'][:, 1], antenna_table['POSITION'][:, 2]
positions = np.column_stack((X, Y, Z))

Arr1 = positions[:, np.newaxis, :] #Adding axis to positions array from (N,3) to (N, 1, 3)
Arr2 = positions[np.newaxis, :, :] #Similar but now converting from (N,3) dimensions to (1, N, 3)

#Calcualting the difference between all pairs of positions (inlcuding with itself as the diagonal which will haev 0's)
diff = Arr1 - Arr2

#Squaring the differences
sqrd_diff = diff**2

#Sum of the squares sum_squares[i,j] = (Xi-Xj)^2 + (Yi-Yj)^2 + (Zi-Zj)^2
sqrd_diff_sum = sqrd_diff.sum(axis=2)

#Distance[i,j] = [ (Xi-Xj)^2 + (Yi-Yj)^2 + (Zi-Zj)^2 ] ^ 0.5
distances = np.sqrt(sqrd_diff_sum) #Finally becoming the distance modulus.

# Getting unique distances, ignoring the diagonal (which are zeros)
# The diagonal is when i == j, so only focusing on upper triangular matrix
# k = offset from diagonal (and thats how 0's are ignored)
triu_indices = np.triu_indices(len(positions), k=1)
unique_distances = distances[triu_indices]

longest_baseline = unique_distances[argmax_more(0, unique_distances)]
shortest_baseline = unique_distances[argmin_more(0, unique_distances)]

print(f"The longest baseline is: {longest_baseline:.4f} meters")
print(f"The shortest baseline is: {shortest_baseline:.4f} meters")

# =============================================================================
# #VISIBLITIY BASELINE plotting:
# =============================================================================
frequencies = spectral_table['CHAN_FREQ'].values.T / 1e6  # Frequencies in MHz

#IMPORTANT:
short_num = 5 #5th shortest
long_num = 12 #12th longest

#Retireving indices of long and short baselines
long_baseline_idx = argmax_more(long_num, unique_distances)
short_baseline_idx = argmin_more(short_num, unique_distances)

# longest_baseline_idx = np.argmax(unique_distances)
# shortest_baseline_idx = np.argmin(unique_distances[-5])

#Getting the actual antenna indices of that baseline
ant1_long, ant2_long = triu_indices[0][long_baseline_idx], triu_indices[1][long_baseline_idx]
ant1_short, ant2_short = triu_indices[0][short_baseline_idx], triu_indices[1][short_baseline_idx]

#FEtching and printing the name of those baselines just to confirmif they are same as was printed a few lines back
ant_name_long_1 = antenna_table["NAME"].values[ant1_long]
ant_name_long_2 = antenna_table["NAME"].values[ant2_long]
ant_name_short_1 = antenna_table["NAME"].values[ant1_short]
ant_name_short_2 = antenna_table["NAME"].values[ant2_short]
print(f'The long baseline is between antennas {ant_name_long_1} and {ant_name_long_2}')
print(f'The short baseline is between antennas {ant_name_short_1} and {ant_name_short_2}')

plot_visibility_data(ant1_short, ant2_short, ant_name_short_1, ant_name_short_2, 
                     f'{str(short_num)}th Shortest', frequencies=frequencies)

plot_visibility_data(ant1_long, ant2_long, ant_name_long_1, ant_name_long_2, 
                     f'{str(long_num)}th Longest', frequencies=frequencies)

# =============================================================================
# Calculating Time Delay
# =============================================================================
#Converting baselines to astropy Quantity
blines = np.array([shortest_baseline, longest_baseline]) * u.m

#Maximum sin(theta) is 1 (when theta = 90 degrees)
max_sin_theta = 1

#Calculate maximum time delay (delta T) for both baselines
max_time_delay = (blines * max_sin_theta / c.c).to(u.ns)

print(f"Maximum Time delay for the shortest baseline: {max_time_delay[0]:.7g}")
print(f"Maximum Time delay for the longest baseline: {max_time_delay[1]:.7g}")

# =============================================================================
# #Plotting time slice of B_long vs B_short
# =============================================================================

#Getting indices of the antennas for the longest and shortest baselines
#byiterating over the unique distances calculated earlier
shortest_index = argmin_more(0, unique_distances)
longest_index = argmax_more(0, unique_distances)

# Get the actual antenna indices corresponding to these distances
# The unique distances indices correspond to the upper triangular matrix
# Use the triu_indices from previous calculations
i, j = triu_indices[0][shortest_index], triu_indices[1][shortest_index]
k, l = triu_indices[0][longest_index], triu_indices[1][longest_index]

# Extract visibility data for the shortest baseline
vis_short = vis[i, :, 0]  # Channel data for the first visibility
vis_long = vis[l, :, 0]   # Channel data for the second visibility

# Plotting the visibility data for the shortest and longest baselines
plt.figure(figsize=(12, 6))

# Shortest baseline plot
plt.plot(np.abs(vis_short), alpha=1,
         label=f'Short Baseline (Antennas {antenna_table["NAME"].values[i]} - {antenna_table["NAME"].values[j]})')
plt.xticks(ticks=np.linspace(0, len(frequencies) - 1,8 ).astype(int), 
           labels=np.round(frequencies.flatten()[::len(frequencies) // 7]))

# Longest baseline plot
plt.plot(np.abs(vis_long), alpha=.7, color="r",
         label=f'Long Baseline (Antennas {antenna_table["NAME"].values[k]} - {antenna_table["NAME"].values[l]})')

plt.semilogy()
plt.xlabel('Frequency [MHz]', labelpad=14)
plt.ylabel('Amplitude')
plt.tight_layout()
plt.legend()
plt.grid(True, which="both")
plt.show()

# =============================================================================
# Identifying specfic RFI for further claculations
# =============================================================================

longest_index = argmax_more(0, unique_distances)
k, l = triu_indices[0][longest_index], triu_indices[1][longest_index]
vis_long = vis[l, :, 0]   # Channel data for the second visibility

plt.figure(figsize=(12, 6))

freq_flat = frequencies.flatten()*u.MHz #An Array of all required frequencies

nearest_frq_index = np.argmin(np.abs(frequencies.flatten() - 1536))
print(f"Found Frequency {freq_flat[nearest_frq_index]} at Channel {nearest_frq_index}")
plt.axvline(x=nearest_frq_index, ymax=1e5, ymin=0, color='r', linestyle='--', alpha=.5)

# Longest baseline plot
plt.plot(np.abs(vis_long), alpha=.7, color="b",
         label=f'Baseline (Antennas {antenna_table["NAME"].values[k]} - {antenna_table["NAME"].values[l]})')

plt.xticks(ticks=np.linspace(0, len(frequencies) - 1,8 ).astype(int), 
           labels=np.round(frequencies.flatten()[::len(frequencies) // 7]))
plt.semilogy()
plt.xlabel('Frequency [MHz]', labelpad=14)
plt.ylabel('Amplitude')
plt.tight_layout()
plt.legend()
plt.grid(True, which="both")
plt.show()

# =============================================================================
# #Getting beam width
# =============================================================================

# Given dish diiametre 
dish_diam = antenna_table["DISH_DIAMETER"][0].compute().to_numpy() * u.meter
freq = freq_flat[nearest_frq_index] #Already carries units

#Conversion of frequecny to wavelngth
wav = c.c / freq

#Aperture illumination factor k (given as 70 for a tapered aperture)
k = 70  # Unitless constant

theta_degrees = (k * (wav / dish_diam)) * u.deg
print(f"Beamwidth theta = {theta_degrees.decompose():.3g}")


# =============================================================================
# Calculating Redshift
# =============================================================================
f_em = 1.4e9*u.Hz  # Emission frequency in Hz (1.4 GHz)

z = (freq / f_em) - 1

print(f"The redshift is: {z:.6f}")
    
theta_radians = theta_degrees.to(u.rad)

# =============================================================================
# # Calculating the frequency spread (Delta f)
# =============================================================================
delta_f = freq * theta_radians.value  # The spread in frequency in Hz

# Number of channels affected
num_channels = (delta_f / (channel_width*u.Hz)).decompose()  # Decomposing into unitless number of channels

print(f"Number of channels affected: {num_channels:.0f}")

# =============================================================================
# Progressive filtering
# =============================================================================

#Accessing Frequency values from spectral table and convertign to MHz
frequencies = spectral_table['CHAN_FREQ'].values.T / 1e6

#Taking visibility amplitudes for the first polarization
visibility_amplitudes = np.abs(vis[:, :, 0])

progressive_rfi_filter(visibility_amplitudes, frequencies)


# In[Histogram]: #RUN THIS CELL ONLY ONCE (MAY TAKE A FEW MINUTES OR TWO)

# =============================================================================
# Histogram of RFI vs Clean
# =============================================================================

#Getting range of antenna indices 0 to 49 (50 antennas)
antenna_indices = np.arange(49)

#Getting all different pairs possible off of those antenna_indices
all_pairs = np.array(np.meshgrid(antenna_indices, antenna_indices)).T.reshape(-1, 2)

#Filtering out pairs where a1 == a2 or where (a2, a1) is a duplicate of (a1, a2)
unique_pairs = all_pairs[all_pairs[:, 0] < all_pairs[:, 1]]

#Initializing lists to store cleaned and RFI data
clean = []
rfi = []

# Loop through unique antenna pairs
for a1, a2 in unique_pairs:
    # Get indices where the current antenna pair matches
    idx = np.where(
        (ds["ANTENNA1"] == a1) & (ds["ANTENNA2"] == a2)
    )[0]

    # # Print antenna names for debugging (optional)
    # print(
    #     antenna_table["NAME"][a1].compute(),
    #     antenna_table["NAME"][a2].compute()
    # )

    # Append the absolute values of relevant dataset slices
    rfi.append(np.abs(ds["DATA"][idx][:, 400,0].compute()))
    clean.append(np.abs(ds["DATA"][idx][:, 600,0].compute()))
    
# In[Making sure it previous section doesnt run again]

plotting_hists(clean, rfi, [1.5,4], ylims=[0,2.5])
plotting_hists(clean, rfi, [0,.1])
