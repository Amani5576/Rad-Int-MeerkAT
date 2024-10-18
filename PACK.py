from daskms import xds_from_table

# Base data path to the measurement set (MS) file
data_path = '/home/amani/Documents/HONOURS_UCT/Second_Semster/Observational_Techniques_2/OT2_Interferometry/'
ms_file = data_path + "1548939342.ms"

ds = xds_from_table(data_path+"1548939342.ms")
ds = dict(ds[0]) #DATASET

# Load each table and convert to difeed_table["RECEPTOR_ANGLE"].compute().to_numpy()[0][0]ctionary
antenna_table = xds_from_table(ms_file + "::ANTENNA")
antenna_table = dict(antenna_table[0])

feed_table = xds_from_table(ms_file + "::FEED")
feed_table = dict(feed_table[0])
receptor_angle = feed_table["RECEPTOR_ANGLE"].compute().to_numpy()[0][0]

field_table = xds_from_table(ms_file + "::FIELD")
field_table = dict(field_table[0])

observation_table = xds_from_table(ms_file + "::OBSERVATION")
observation_table = dict(observation_table[0])

polarization_table = xds_from_table(ms_file + "::POLARIZATION")
polarization_table = dict(polarization_table[0])

processor_table = xds_from_table(ms_file + "::PROCESSOR")
processor_table = dict(processor_table[0])

source_table = xds_from_table(ms_file + "::SOURCE")
source_table = dict(source_table[0])

spectral_window_table = xds_from_table(ms_file + "::SPECTRAL_WINDOW")
spectral_window_table = dict(spectral_window_table[0])

state_table = xds_from_table(ms_file + "::STATE")
state_table = dict(state_table[0])

params = {
        'legend.fontsize': 'x-large',
        'figure.figsize': (12, 10),
        'axes.labelsize': 13,
        'axes.titlesize':13,
        'xtick.labelsize':13,
        'ytick.labelsize':13,
        'axes.labelweight':'bold',
        'font.size':13,
        'figure.max_open_warning': 0
        }

channel_width = spectral_window_table['CHAN_WIDTH'].values[0][0]
frequencies = spectral_window_table['CHAN_FREQ'].values
nchannels = spectral_window_table['NUM_CHAN'].values[0]
