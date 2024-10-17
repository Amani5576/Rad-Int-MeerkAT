from daskms import xds_from_table
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#---------------------------------------------------------------------------------------------------------

data_path = "/home/aidan/Desktop/OT2/Assignment 2/"
ds = xds_from_table(data_path+"1548939342.ms")
ds = dict(ds[0])
antenna_table = xds_from_table(data_path+"1548939342.ms::ANTENNA")
antenna_table = dict(antenna_table[0])
obs_table = xds_from_table(data_path+"1548939342.ms::OBSERVATION")
obs_table = dict(obs_table[0])

#Getting range of antenna indices 0 to 49 (50 antennas)
antenna_indices = np.arange(49)

#Getting all different pairs possible off of those antenna_indices
all_pairs = np.array(np.meshgrid(antenna_indices, antenna_indices)).T.reshape(-1, 2)

#Filtering out pairs where a1 == a2 or where (a2, a1) is a duplicate of (a1, a2)
unique_pairs = all_pairs[all_pairs[:, 0] < all_pairs[:, 1]]

# # Initialize lists to store cleaned and RFI data
# vis_clean = []
# vis_rfi = []

# counter = 0
# # Loop through unique antenna pairs
# for a1, a2 in unique_pairs:
#     # Get indices where the current antenna pair matches
#     idx = np.where((ds["ANTENNA1"] == a1) & (ds["ANTENNA2"] == a2))[0]

#     # # Print antenna names for debugging (optional)
#     # print(antenna_table["NAME"][a1].compute(),
#     #     antenna_table["NAME"][a2].compute())

#     # Append the absolute values of relevant dataset slices
#     vis_rfi.append(np.abs(ds["DATA"][idx][:, 400,0].compute()))
#     vis_clean.append(np.abs(ds["DATA"][idx][:, 600,0].compute()))
    
#     print(counter)
#     counter = counter+1
    
# # In[Making sure it doesnt rerun again]

# # Concatenate the lists into arrays
# combined_array_clean = np.concatenate(vis_clean)
# combined_array_rfi = np.concatenate(vis_rfi)

#---------------------------------------------------------------------------------------------------------

# # Save the Array to a Text File
# np.savetxt("combined_array_clean_data.txt", combined_array_clean, delimiter=',', fmt='%f')
# np.savetxt("combined_array_rfi_data.txt", combined_array_rfi, delimiter=",", fmt='%f')

#---------------------------------------------------------------------------------------------------------

# Load data from Text File into Numpy Array
combined_array_clean = np.loadtxt("/home/aidan/Desktop/OT2/Assignment 2/combined_array_clean_data.txt", delimiter=',')
combined_array_rfi = np.loadtxt("/home/aidan/Desktop/OT2/Assignment 2/combined_array_rfi_data.txt", delimiter=",")

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

#---------------------------------------------------------------------------------------------------------

def gaussian(x,A,x0,sigma,D):                      # gaussian fnc
    # A = amplitude = peak flux - continuum flux
    # x0 = central wavelength/mean
    # sigma = standard deviation
    # D = continuum flux
    return D+A*np.exp(-((x-x0)**2)/(2*(sigma**2)))

def gauss_fit(x,y,guess):                   # calculate gaussian best fit parameters
    params,covariance = curve_fit(gaussian,x,y,p0=guess)
    return params

#---------------------------------------------------------------------------------------------------------

def plotting_hists(ini_guess_rfi, ini_guess_clean, xlims, ylims=[0,]):
    n_bins = 500
    plt.figure(figsize=(16,10))
    # Plot Histograms
    cleancounts,cleanbins,cleanbars = plt.hist(combined_array_clean, bins=n_bins, alpha=0.5, histtype=u'step', lw=2, density=True, label='Clean Data')
    rficounts,rfibins,rfibars = plt.hist(combined_array_rfi, bins=n_bins, alpha=0.5, histtype=u'step', lw=2, density=True, label='RFI Data')
    # plt.show()

    # Find x-limits Indices & Slice Data Arrays
    x_low,x_high = xlims[0],xlims[1]
    indices_clean = np.where((cleanbins > x_low) & (cleanbins < x_high))
    indices_rfi = np.where((rfibins > x_low) & (rfibins < x_high))

    cleanbins = cleanbins[np.min(indices_clean):np.max(indices_clean)]
    cleancounts = cleancounts[np.min(indices_clean):np.max(indices_clean)]
    rfibins = rfibins[np.min(indices_rfi):np.max(indices_rfi)]
    rficounts = rficounts[np.min(indices_rfi):np.max(indices_rfi)]

    # plt.plot(cleanbins,cleancounts,label="Clean Data",marker="x")
    # plt.plot(rfibins,rficounts,label="RFI Data",marker="x")

    # Create x-arrays for Gaussian Fits
    gaussx_rfi = np.linspace(np.min(rfibins),np.max(rfibins),1000)
    gaussx_clean = np.linspace(np.min(cleanbins),np.max(cleanbins),1000)

    # Get Gaussian Parameters
    rfiparams = gauss_fit(rfibins,rficounts,ini_guess_rfi)
    cleanparams = gauss_fit(cleanbins,cleancounts,ini_guess_clean)

    # Plot Best Fit Gaussians
    plt.plot(gaussx_rfi,gaussian(gaussx_rfi,*rfiparams),label="RFI Gaussian Fit")
    plt.plot(gaussx_clean,gaussian(gaussx_clean,*cleanparams),label="Clean Gaussian Fit")
  
    plt.xlabel('Amplitude', fontsize=22,labelpad=30)
    plt.ylabel('Counts',fontsize=22,labelpad=30)
    plt.legend(loc='upper right',fontsize=28)
    plt.xlim(*xlims)
    plt.ylim(*ylims)
    plt.show()

    # Print Fit Attributes
    print("RFI")
    print("RFI Stnd Dev: ",rfiparams[2])
    print("RFI Mean:     ",rfiparams[1])
    print("RFI Skewness: ",skew(gaussian(gaussx_rfi,*rfiparams)))
    print("RFI Kurtosis: ",kurt(gaussian(gaussx_rfi,*rfiparams)))

    print("")
    print("CLN")
    print("CLN Stnd Dev: ",cleanparams[2])
    print("CLN Mean:     ",cleanparams[1])
    print("CLN Skewness: ",skew(gaussian(gaussx_clean,*cleanparams)))
    print("CLN Kurtosis: ",kurt(gaussian(gaussx_clean,*cleanparams)))

#---------------------------------------------------------------------------------------------------------

guess_rfi = [2,2.3,0.5,0]
guess_clean = [1.3,2.3,0.5,0]
plotting_hists(guess_rfi, guess_clean, [1.5,4], ylims=[0,2.5])
 
# guess_rfi = [2.8,0.007,0.007,0]
# guess_clean = [4.525,0.004,0.004,0]
# plotting_hists(guess_rfi, guess_clean, [0.004,0.1], [0,5])

#--------------------------------------------------------------------------------------------------------