'''
Utility functions to return data from abf files.
'''

import numpy as np
import quantities as pq
import matplotlib.pyplot as plt
from neo.io import AxonIO
import os
import argparse

def expdata(Address, Index=0, mode='Iclamp'):
    """
    Load electrophysiology data from either '.abf' or '.dat' files.
    
    Parameters:
    - Address (str): File path to the data file (either .abf or .dat).
    - Index (int): Index to specify which trace to extract if there are multiple traces.
                   Defaults to 0 (first trace).
    - mode (str): Mode of recording - 'Iclamp' (current clamp) or 'Vclamp' (voltage clamp).
                  Determines whether voltage or current data is returned.
    
    Returns:
    - A list containing:
        1. Time vector (in seconds).
        2. Voltage data (in volts) if mode is 'Iclamp'.
           Current data (in amperes) if mode is 'Vclamp'.
    """
    
    # Determine the file extension to decide how to process the data.
    file_extension = os.path.splitext(Address)[1]
    
    # Check if the file is an Axon Binary File (.abf)
    if file_extension == '.abf':
        # Read the .abf file using the AxonIO class from the NEO library
        reader = AxonIO(filename=Address)
        Samprate = reader.get_signal_sampling_rate()  # Sampling rate in Hz
        
        # Read the specified segment (trace) from the file
        # `signal_group_mode='split-all'` ensures each channel is read separately
        seg = reader.read_block(signal_group_mode='split-all').segments[Index]
        
        # Calculate the total duration of the recording (in seconds)
        Tdur = np.array(seg.t_stop - seg.t_start)
        
        # If in current clamp mode ('Iclamp'), return the voltage trace
        if mode == 'Iclamp':
            # Extract voltage signal and convert to volts (originally in millivolts)
            V = np.array(np.ravel(seg.analogsignals[0])) * 1e-3
            # Generate a time vector from 0 to the total duration
            return [np.linspace(0, Tdur, len(V)), V]
        
        # If in voltage clamp mode ('Vclamp'), return the current trace
        elif mode == 'Vclamp':
            # Extract current signal and convert to amperes (originally in picoamperes)
            I = np.array(np.ravel(seg.analogsignals[0])) * 1e-12
            # Generate a time vector from 0 to the total duration
            return [np.linspace(0, Tdur, len(I)), I]
    
    # Check if the file is a .dat file
    elif file_extension == '.dat':
        # Load data from the .dat file using numpy
        # Each row corresponds to time and subsequent columns to different channels
        data = np.loadtxt(Address)
        
        # Transpose the data matrix so that rows correspond to time and channels
        transposed_data = np.transpose(data)
        
        # The first row is the time vector (in seconds)
        T = transposed_data[0]
        
        # For current clamp mode ('Iclamp'), extract the voltage trace
        if mode == 'Iclamp':
            # Extract the voltage data for the specified Index and convert to volts
            V = transposed_data[1:][Index] * 1e-3
            return [T, V]
        
        # For voltage clamp mode ('Vclamp'), extract the current trace
        elif mode == 'Vclamp':
            # Extract the current data for the specified Index and convert to amperes
            I = transposed_data[1:][Index] * 1e-12
            return [T, I]
    
    # If the file extension is not recognized, raise an error
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Expected '.abf' or '.dat'.")


def plotexp(Address, Index=0, mode='Iclamp', Title='Current clamp at 150pA'):
    """
    Plot electrophysiology data for either current clamp or voltage clamp recordings.
    
    Parameters:
    - Address (str): File path to the data file (either .abf or .dat).
    - Index (int): Index to specify which trace to extract if there are multiple traces.
                   Defaults to 0 (first trace).
    - mode (str): Mode of recording - 'Iclamp' (current clamp) or 'Vclamp' (voltage clamp).
    - Title (str): Title for the plot.
    
    Returns:
    - None. Displays a plot of the recorded data.
    """
    
    # Check if the mode is 'Iclamp' (current clamp)
    if mode == 'Iclamp':
        # Load time and voltage data using the expdata function
        T, V = expdata(Address, Index, mode)
        
        # Plot the voltage trace with a baseline offset adjustment of -0.016V
        plt.plot(T, V - 0.016, label=Address)
        
        # Add plot details
        plt.legend()
        plt.title(Title)
        plt.xlabel('Time (s)')
        plt.ylabel('Membrane potential (V)')
        plt.show()
    
    # Check if the mode is 'Vclamp' (voltage clamp)
    elif mode == 'Vclamp':
        # Load time and current data using the expdata function
        T, I = expdata(Address, Index, mode)
        
        # Plot the current trace as is
        plt.plot(T, I, label=Address)
        
        # Add plot details
        plt.legend()
        plt.title(Title)
        plt.xlabel('Time (s)')
        plt.ylabel('Holding current (A)')
        plt.show()
    
    # If an unsupported mode is provided, raise an error
    else:
        raise ValueError("Unsupported mode. Please use 'Iclamp' or 'Vclamp'.")


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Load and plot electrophysiology data from multiple files.')
    
    parser.add_argument('Addresses', type=str, nargs='+',
                        help='Paths to the data files (.abf or .dat). You can specify multiple files.')
    parser.add_argument('--Index', type=int, default=0, help='Index of the trace to extract (default: 0)')
    parser.add_argument('--mode', type=str, choices=['Iclamp', 'Vclamp'], default='Iclamp',
                        help="Recording mode: 'Iclamp' for current clamp, 'Vclamp' for voltage clamp")
    parser.add_argument('--Title', type=str, default='Electrophysiology Plot',
                        help='Title for the plot')
    
    args = parser.parse_args()
    
    # Loop through each file and plot its data
    for address in args.Addresses:
        try:
            plotexp(Address=address, Index=args.Index, mode=args.mode, Title=args.Title)
        except Exception as e:
            print(f"Error processing {address}: {e}")

