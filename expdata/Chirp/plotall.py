from neo.io import AxonIO  # For reading .abf (Axon Binary Files) data
import numpy as np
import sys
import matplotlib.pyplot as plt  # For plotting
import os
import argparse
import tkinter as tk  # For creating a graphical file dialog
from tkinter import filedialog  # To browse and select folders
import gc  # For garbage collection

# Main function to load, process, and plot electrophysiology data
def main():
    """
    Main function to browse a directory, read .abf and .dat files, plot the data, 
    and save the resulting figures as PNG images. Ensures existing plots are not overwritten.
    """
    # Initialize Tkinter root and hide the main window
    root = tk.Tk()
    root.withdraw()
    
    # Open a dialog to select a directory containing the data files
    folder_path = filedialog.askdirectory()
    
    # List to store the paths of valid files
    filegenerator = []
    
    # Recursively walk through the selected folder to find all files
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            # Construct the absolute file path
            tempfilename = os.path.abspath(os.path.join(dirpath, f))
            
            # Check if the file is either a .abf or .dat file
            if os.path.splitext(tempfilename)[1] == '.abf' or os.path.splitext(tempfilename)[1] == '.dat':
                filegenerator.append(tempfilename)

    # Process each valid file
    for file in filegenerator:
        print(f"Processing file: {file}")
        splitted = os.path.splitext(file)
        
        # Handle .abf files
        if os.path.splitext(file)[1] == '.abf':
            # Check if a plot for this file already exists to avoid overwriting
            if os.path.isfile(file[:-4]+'_Anal.png') or os.path.isfile(file[:-4]+'_Anal.jpg') or os.path.isfile(file[:-4]+'_Anal.jpeg'):
                print(f"{file[:-4]}_Anal.png already exists. Skipping.")
                continue
            
            # Create a new figure for plotting
            fig, axs = plt.subplots(1, 1, figsize=(19.20, 10.80))
            
            # Read the .abf file using AxonIO
            reader = AxonIO(filename=file)
            Samprate = reader.get_signal_sampling_rate()  # Get the sampling rate
            
            # Loop through each segment in the .abf file and plot the data
            for seg in reader.read_block(signal_group_mode='split-all').segments:
                Tdur = np.array(seg.t_stop - seg.t_start)  # Duration of the segment
                V = np.array(np.ravel(seg.analogsignals[0]))  # Extract voltage data
                axs.plot(np.linspace(0, Tdur, len(V)), V)  # Plot time vs. voltage
            
            # Set the title to the filename (without extension)
            fig.suptitle(os.path.splitext(os.path.basename(file))[0])
            
            # Save the plot as a PNG file
            fig.savefig(splitted[0]+'_Anal.png')
            plt.close()
        
        # Handle .dat files
        elif os.path.splitext(file)[1] == '.dat':
            # Check if a plot for this file already exists to avoid overwriting
            if os.path.isfile(file[:-4]+'_Anal.png') or os.path.isfile(file[:-4]+'_Anal.jpg') or os.path.isfile(file[:-4]+'_Anal.jpeg'):
                print(f"{file[:-4]}_Anal.png already exists. Skipping.")
                continue
            
            try:
                # Create a new figure for plotting
                fig, axs = plt.subplots(1, 1, figsize=(19.20, 10.80))
                
                # Load data from the .dat file
                a = np.loadtxt(file)
                b = np.transpose(a)  # Transpose to access time and channels separately
                
                # Plot time vs. data (all channels)
                axs.plot(b[0], np.transpose(b[1:]))
                
                # Set the title to the filename (without extension)
                fig.suptitle(os.path.splitext(os.path.basename(file))[0])
                
                # Save the plot as a PNG file
                fig.savefig(splitted[0]+'_Anal.png')
                plt.close()
            
            # Handle any errors that occur while processing the .dat file
            except Exception as e:
                print(f"########\n{file} skipped due to error: {e}\n#########")

# Entry point for the script
if __name__ == '__main__':
    main()
