import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.signal import medfilt
from PACK import ds

def argmax_more(num, arr):  # Gets the num-th maximum index in the array
    sorted_indices = np.argsort(arr)
    if num < 0 or num >= len(arr):
        raise ValueError("num must be in the range 0 to len(arr)-1")
    return sorted_indices[-(num + 1)]  # Access the num-th maximum

def argmin_more(num, arr):  # Gets the num-th minimum index in the array
    sorted_indices = np.argsort(arr)
    if num < 0 or num >= len(arr):
        raise ValueError("num must be in the range 0 to len(arr)-1")
    return sorted_indices[num]  # Access the num-th minimum

def plot_visibility_data(a1, a2, name1, name2, baseline_type, frequencies):
    # Find the indices for the specific antennas
    idx = np.where((ds["ANTENNA1"] == a1) & (ds["ANTENNA2"] == a2))[0]
    
    # Plot frequency against time for the baseline
    plt.figure()
    plt.imshow(np.abs(ds["DATA"][idx][:,:, 0]).T,
               aspect='auto',
               cmap="Spectral",
               origin="lower",
               norm=colors.LogNorm())

    #Setting frequency as y axis instead f channels, with a total of 10 labels
    plt.yticks(ticks=np.linspace(0, len(frequencies) - 1, 10).astype(int),
               labels=np.round(frequencies.flatten()[::len(frequencies) // 9],0))

    ls, lp = 25, 20
    plt.ylabel('Frequency (MHz)', fontsize=ls, labelpad=lp)
    plt.xlabel('Time', fontsize=ls, labelpad=lp)
    cbar = plt.colorbar(label=r"$\log(\text{Visibility Amplitude})$")
    cbar.set_label(r"$\log(\text{Visibility Amplitude})$", fontsize=24, labelpad=2)    
    plt.title(f'{baseline_type} Baseline (Antennas {name1} & {name2})', fontsize=27, pad=15)
    plt.tight_layout()
    plt.show()

def progressive_rfi_filter(visibility_amplitudes, frequencies, initial_kernel=29, sigma_threshold=1):

    """
    Progressive median filter for RFI detection, starting with a large kernel size
    and progressively decreasing it until no further RFI is detected.
    
    Parameters:
    - visibility_amplitudes: The visibility amplitude data (2D array with shape [time, frequency]).
    - frequencies: The frequency values (1D array).
    - initial_kernel: The starting size for the median filter kernel (default 40).
    - sigma_threshold: The threshold for RFI detection in terms of standard deviation (default 5).
    """
    
    #Extracting visibility data at a specific time frame
    data = visibility_amplitudes[500, :]  #Initial data to be preogressively will be progressively filtered
    
    # Keep track of kernel size and iteration
    kernel_size = initial_kernel
    iteration = 1
    
    # Set up the figure for plotting
    plt.figure(figsize=(14, 18))
    plt.subplot(5, 1, 1)
    plt.plot(frequencies, data, label="Original Visibility")
    plt.title("Original Visibility Data at Time Frame 500")
    plt.ylabel("Amplitude", labelpad=20, fontsize=20)
    plt.grid(True, which="both")
    plt.legend()

    while True: #Avoiding kernal from being too small
        # Apply median filter
        smoothed_data = medfilt(data, kernel_size)
        
        #Getting absolute STD from smoothed data in comparison to previous
        deviation = np.abs(data - smoothed_data)
        threshold = sigma_threshold * np.std(deviation) #Creating limit where RFI should ideally surpass it
        
        #Identifying indices where RFI is likely present
        rfi_indices = np.where(deviation > threshold)[0]
        
        plt.subplot(4, 1, iteration + 1)
        plt.plot(frequencies, data, label="Previous Data Before Filtering")
        plt.plot(frequencies, smoothed_data, label=f"Smoothed Data (Kernel size = {kernel_size})", linestyle='--')
        plt.scatter(frequencies[rfi_indices], data[rfi_indices], color='red', label='Detected RFI', zorder=5, s=5, marker="s")
        plt.title(f"RFI Detection with Kernel Size {kernel_size}")
        plt.ylabel("Amplitude", labelpad=20, fontsize=20)
        plt.grid(True, which="both")
        plt.legend()

        # If no RFI is detected, then thats enough smooothing (Otherwaise its just oversmoothing from this point onwards)
        if len(rfi_indices) == 0:
            print(f"No more RFI detected after kernel size {kernel_size}. Stopping.")
            break
        
        #In next loop, smooth the data further by making output data the previous (original) data
        data = smoothed_data
        
        #Decrementation of the kernel size (ensuring it remains odd)
        kernel_size /= 5
        kernel_size = int(kernel_size)
        if kernel_size % 2 == 0:
            kernel_size -= 1  #Ensuring the kernel size remains odd
        
        iteration += 1 #Jsut a subplot iterator
        
        if iteration >= 5: #Avoding to plot too many subplots.
            print("Dont want too many subplots")
            break

        if kernel_size <= 3: kernel_size ==3
        
    plt.xlabel("Frequency", labelpad=20, fontsize=20)
    plt.tight_layout()
    plt.show()
    
def plotting_hists(vis_clean, vis_rfi, xlims, ylims=[0,]):
    # Concatenate the lists into arrays
    combined_array_clean = np.concatenate(vis_clean)
    combined_array_rfi = np.concatenate(vis_rfi)

    plt.figure(figsize=(16,10))
    # Plot histograms
    plt.hist(
        combined_array_clean, bins=500, alpha=0.5, 
        histtype=u'step', lw=2, density=True, label='Clean Data'
    )
    plt.hist(
        combined_array_rfi, bins=500, alpha=0.5, 
        histtype=u'step', lw=2, density=True, label='RFI Data'
    )
    
    # Customize plot appearance
    plt.xlabel('Amplitude', fontsize=22, labelpad=30)
    plt.ylabel('Counts',fontsize=22, labelpad=30)
    plt.legend(loc='upper right', fontsize=28)
    plt.xlim(*xlims)
    plt.ylim(*ylims)
    plt.show()