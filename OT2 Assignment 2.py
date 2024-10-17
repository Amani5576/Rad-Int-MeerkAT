# OT2 ASSIGNMENT #2
# MRTAID003
# October 2024

#---------------------------------------------------------------------------------------------------------

# conda deactivate
# conda create -n daskms python=3.12
# conda activate daskms
# https://dask-ms.readthedocs.io/en/latest/readme.html#installation
# conda install ipykernel 

# in VSCode, change kernel to "daskms" (top RHS in .ipynb, bottom RHS in .py)

#---------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib import colors 
from matplotlib.colors import LogNorm
import dask.array as da
from daskms import xds_from_table
from dask.distributed import Client
import numpy as np
from astropy.time import Time
import statistics
from scipy.optimize import curve_fit
from statsmodels.stats.weightstats import DescrStatsW
from scipy.signal import detrend

#---------------------------------------------------------------------------------------------------------
# Q1
#---------------------------------------------------------------------------------------------------------

data_path = "/home/aidan/Desktop/OT2/Assignment 2/"
ds = xds_from_table(data_path+"1548939342.ms")

#---------------------------------------------------------------------------------------------------------

data_des = xds_from_table(data_path+"1548939342.ms::SOURCE")
object_name = data_des[0]['NAME'].values        # Object Name

#---------------------------------------------------------------------------------------------------------

obs_table = xds_from_table(data_path+"1548939342.ms::OBSERVATION")

# for key in obs_table[0].keys():
#     print(f'{key}: {obs_table[0][key].values}')

# print(f'{'TIME_RANGE'}: {obs_table[0]['TIME_RANGE'].values}')
start_end_times = obs_table[0]['TIME_RANGE'].values
datastarttime = start_end_times[0][0]
dataendtime = start_end_times[0][1]
# print(datastarttime,dataendtime)

# START TIME/ END TIME
timestamp_start = datastarttime/(60*60*24)
timestamp_end = dataendtime/(60*60*24)
time_start = Time(timestamp_start, format="mjd")
time_end = Time(timestamp_end, format="mjd")
utc_time_start = time_start.utc     # Convert to UTC
utc_time_end = time_end.utc         # Convert to UTC

#---------------------------------------------------------------------------------------------------------

A1 = ds[0]["ANTENNA1"]
A2 = ds[0]["ANTENNA2"]
ant_list = list(set(np.append(A1,A2)))
nants = len(ant_list)
inter = ds[0]["INTERVAL"]

#---------------------------------------------------------------------------------------------------------

spectral_table = xds_from_table(data_path+"1548939342.ms::SPECTRAL_WINDOW")

frequencies = spectral_table[0]['CHAN_FREQ'].values
nchannels = spectral_table[0]['NUM_CHAN'].values[0]
channel_width = spectral_table[0]['CHAN_WIDTH'].values[0][0]

summary = {
    'Frequencies': frequencies,
    'No_Channeles': nchannels,
    'Channel_Width': channel_width,
    }

#---------------------------------------------------------------------------------------------------------

print("Object Name: ", object_name)
print("Start Time:", utc_time_start.iso)
print("End Time:  ", utc_time_end.iso)
print(f'Total number of antennas used: {nants}')
# print('Interval Table Shape: ',inter.shape)
# print(f'Dump rate is {np.median(inter)} s');
print(f"Frequency range (MHz): {summary['Frequencies'].min()/1.e6} - {summary['Frequencies'].max()/1.e6}")  
# print(f"Total no of channels: {summary['No_Channeles']}")
print(f"Channel width (kHz): {channel_width/1.e3}")
print()

#---------------------------------------------------------------------------------------------------------
# Q2
#---------------------------------------------------------------------------------------------------------

u,v,w = ds[0]['UVW'][:,0],ds[0]['UVW'][:,1],ds[0]['UVW'][:,2]

plotting = "no"
if plotting == "yes":               # UVW Plotting
    plt.figure(figsize=(8,8))
    plt.plot(u,v,'.')
    plt.title("PKS1934-63 UV Coverage",fontsize=16)
    plt.xlabel('u',fontsize=14)
    plt.ylabel('v',fontsize=14)
    plt.show()

#---------------------------------------------------------------------------------------------------------

antenna_table = xds_from_table(data_path+"1548939342.ms::ANTENNA")

# print(antenna_table[0]['NAME'].values)
# print(antenna_table[0]['DISH_DIAMETER'].values)
# print(antenna_table[0]['POSITION'].values)
# print(antenna_table[0]['POSITION'].values[-1][0])

# l = []
# ij = []
# for i in range(len(antenna_table[0]['POSITION'].values)):
#     for j in range(i+1,len(antenna_table[0]['POSITION'].values)):

#         ix = antenna_table[0]['POSITION'].values[i][0]      # Antennae positions (x,y,z)
#         iy = antenna_table[0]['POSITION'].values[i][1]
#         iz = antenna_table[0]['POSITION'].values[i][2]
#         jx = antenna_table[0]['POSITION'].values[j][0]
#         jy = antenna_table[0]['POSITION'].values[j][1]
#         jz = antenna_table[0]['POSITION'].values[j][2]

#         dist = ((ix-jx)**2+(iy-jy)**2+(iz-jz)**2)**(1/2)    # Distance between 2 antennae
#         l.append(dist)
#         ij.append([i,j])
#         # print(f"({i}, {j}): {dist}")

# print(l)                                                    # Baseline Distances
# print(ij)                                                   # Antennae Pairings
# print("Smallest Baseline:", round(np.min(l),3),"m")         # Minimum & Maximum Baselines
# print("Largest Baseline:", round(np.max(l),3),"m")
# print(np.argmin(l),np.argmax(l))                            # Minimum & Maximum Baselines Argument 
# print(ij[np.argmin(l)],ij[np.argmax(l)])                    # Antennae Pairings with Smallest/Largest Baselines 

# min1,min2 = ij[np.argmin(l)][0], ij[np.argmin(l)][1]
# max1,max2 = ij[np.argmax(l)][0], ij[np.argmax(l)][1]

# print(f"Smallest Baseline Antennae Pair: ({antenna_table[0]['NAME'].values[min1]},{antenna_table[0]['NAME'].values[min2]})")
# print(f"Largest Baseline Antennae Pair: ({antenna_table[0]['NAME'].values[max1]},{antenna_table[0]['NAME'].values[max2]})")


#---------------------------------------------------------------------------------------------------------

X,Y,Z = antenna_table[0]['POSITION'][:,0],antenna_table[0]['POSITION'][:,1],antenna_table[0]['POSITION'][:,2]

plotting = "no"             # XYZ Plotting
if plotting == "yes":
    plt.figure(figsize=(9,9))
    plt.plot(X,Y, 'o')
    plt.show()

#---------------------------------------------------------------------------------------------------------
# Q3
#---------------------------------------------------------------------------------------------------------

vis = ds[0]['DATA']
# print(vis.shape)

imshowplotting = "yes"
if imshowplotting == "yes":
    plt.imshow(np.abs(vis[:,:,0]).T, 
               aspect= 'auto', 
               origin='lower', 
               cmap='PuOr', 
               norm = colors.LogNorm()
               );
    plt.ylabel('Channel No',fontsize=14)
    plt.xlabel('Time',fontsize=14)
    plt.colorbar()
    plt.show()

    plt.imshow(np.abs(vis[:,:,1]).T, 
               aspect= 'auto', 
               origin='lower',
               cmap='PuOr', 
               norm = colors.LogNorm()
               );
    plt.ylabel('Channel No',fontsize=14)
    plt.xlabel('Time',fontsize=14)
    plt.colorbar()
    plt.show()

#---------------------------------------------------------------------------------------------------------

n = 500
phaset2selected = np.angle(vis[n,:,0].T)

#---------------------------------------------------------------------------------------------------------

plotting = "no"
if plotting == "yes":
    # 1-D cut across the visibility 
    plt.plot(np.abs(vis[n,:,0]))
    plt.semilogy()
    plt.ylabel('Amplitude')
    plt.xlabel('Channels')
    plt.show()

plotting = "no"
if plotting == "yes":
    plt.plot(phaset2selected)
    plt.ylabel('Phase')
    plt.xlabel('Channel')
    plt.show()

plotting = "no"
if plotting == "yes":
    plt.plot(np.unwrap(phaset2selected))
    plt.ylabel('Phase')
    plt.xlabel('Channel')
    plt.show()

#---------------------------------------------------------------------------------------------------------

def gaussian(x,A,x0,sigma,D):                      # gaussian fnc
    # A = amplitude = peak flux - continuum flux
    # x0 = central wavelength
    # sigma = standard deviation
    # D = continuum flux
    return D+A*np.exp(-((x-x0)**2)/(2*(sigma**2)))

def gauss_fit(x,y,guess):                   # calculate gaussian best fit parameters
    params,covariance = curve_fit(gaussian,x,y,p0=guess)
    return params

#---------------------------------------------------------------------------------------------------------

# Plot the average across frequency slice
frequencies = spectral_table[0]['CHAN_FREQ'].values.T
absdata = np.abs(vis[n,:,0]).compute()
# print(frequencies[0]/1.e6,frequencies[-1]/1.e6)

plotting = "no"                    # visibility slice w/ frequency
if plotting == "yes":
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    ax1.plot(frequencies/1.e6,np.log10(absdata),'-')
    ax1.set_xticks(np.arange(frequencies[0]/1.e6,frequencies[-1]/1.e6, step=100))
    ax1.set_xlabel('Frequency [MHz]',fontsize=14)
    ax1.set_ylabel('Amplitude',fontsize=14)

    ax2.plot(np.log10(absdata))
    ax2.set_xticks(np.arange(0,absdata.shape[0], step=256))
    ax2.set_xlabel('Index no',fontsize=14)
    plt.grid()
    plt.show()

#---------------------------------------------------------------------------------------------------------

RFIfreq = frequencies[334:538]      # centre RFI region slice 
RFIabsdata = absdata[334:538]       # centre RFI region slice
cleanfreq = frequencies[538:795]    # clean region slice
cleanasbdata = absdata[538:795]     # clean region slice

#---------------------------------------------------------------------------------------------------------

plotting = "no"
if plotting == "yes":
    n_bins = 50
    fig,axs = plt.subplots(1,2,tight_layout=True)
    RFIcounts,RFIbins,RFIbars = axs[0].hist(np.log10(RFIabsdata), bins=n_bins)
    axs[0].set_title("RFI Region (Channel 334-538)",fontsize=16)
    axs[0].set_xlabel('Amplitude',fontsize=14)
    axs[0].set_ylabel('Frequencies (#)',fontsize=14)

    cleancounts,cleanbins,cleanbars = axs[1].hist(np.log10(cleanasbdata), bins=n_bins)
    axs[1].set_title("Clean Region (Channel 538-795)",fontsize=16)
    axs[1].set_xlabel('Amplitude',fontsize=14)
    axs[0].set_ylabel('Frequencies (#)',fontsize=14)
    
    gaussx = np.linspace(np.min(RFIbins),np.max(RFIbins),1000)  # Gaussian Fitting
    RFIbins = RFIbins[0:-1:1]
    cleanbins = cleanbins[0:-1:1]
    ini_guess = [42,0.5,0.7,0]
    RFIparams = gauss_fit(RFIbins,RFIcounts,ini_guess)
    # print(RFIparams)
    axs[0].plot(gaussx,gaussian(gaussx,*RFIparams))
    
    plt.show()

# print("RFI")
# print("stdev:", np.std(RFIbins))
# print("weighted stdev:", DescrStatsW(RFIbins, weights=RFIcounts, ddof=1).std)
# print("median: ", statistics.median(RFIbins))
# print("range:", np.max(RFIbins)-np.min(RFIbins))
# print("CLEAN")
# print("stdev:", np.std(cleanbins))
# print("weighted stdev:", DescrStatsW(cleanbins, weights=cleancounts, ddof=1).std)
# print("median: ", statistics.median(cleanbins))
# print("range:", np.max(cleanbins)-np.min(cleanbins))

#---------------------------------------------------------------------------------------------------------

def skew(distribution):     # calculate skewness
   n = len(distribution)
   mean = np.mean(distribution)
   std = np.std(distribution)

   a = n/((n-1)*(n-2))
   b = np.sum(((distribution-mean)/std)**3)
   skewness = a*b
   return skewness

def kurt(distribution):     # calculate kurtosis
   n = len(distribution)
   mean = np.mean(distribution)
   std = np.std(distribution)

   kurtosis = (1/n)*sum(((distribution-mean)/std)**4)-3
   return kurtosis

# print("RFI Skewness: ",skew(gaussian(gaussx,*RFIparams)))
# print("CLN Skewness: ",skew(cleancounts))
# print("RFI Kurtosis: ",kurt(gaussian(gaussx,*RFIparams)))
# print("CLN Kurtosis: ",kurt(cleancounts))

#---------------------------------------------------------------------------------------------------------

harmonicfreq = frequencies[956:-1]
# print(frequencies[956]/1.e6,frequencies[-1]/1.e6)
harmonicdata = absdata[956:-1]
x = 1683*np.ones(20)
y = np.linspace(np.min(np.log10(harmonicdata))-0.02,np.max(np.log10(harmonicdata))+0.02,20)

plotting = "no"
if plotting == "yes":
    plt.plot(harmonicfreq/1.e6,np.log10(harmonicdata),label="Data")
    plt.plot(x,y,label="153 MHz 11th Harmonic (1683 MHz)")
    plt.title("Channel 956-1024 (1655.156-1711.164 MHz)",fontsize=16)
    plt.xlabel('Frequency [MHz]',fontsize=14)
    plt.ylabel('Amplitude',fontsize=14)
    plt.legend(fontsize=12)
    plt.show()

#---------------------------------------------------------------------------------------------------------

detrended = detrend(absdata,type="linear")
trend = absdata - detrended

plotting = "no"                    # detrended visibility slice w/ frequency
if plotting == "yes":
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    ax1.plot(frequencies/1.e6,np.log10(absdata),'-',label="Data")
    ax1.plot(frequencies/1.e6,np.log10(trend),'-',label="Detrended Data")
    ax1.set_xticks(np.arange(frequencies[0]/1.e6,frequencies[-1]/1.e6, step=100))
    ax1.set_xlabel('Frequency [MHz]',fontsize=14)
    ax1.set_ylabel('Amplitude',fontsize=14)
    ax1.legend(fontsize=12)

    ax2.plot(np.log10(absdata))
    ax2.set_xticks(np.arange(0,absdata.shape[0], step=256))
    ax2.set_xlabel('Index no',fontsize=14)
    
    plt.grid()
    plt.show()

#---------------------------------------------------------------------------------------------------------


