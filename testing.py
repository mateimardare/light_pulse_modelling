#this script is mainly for testing comm
#also for experoimenting or addinf new fieatures (testing plm)
#every functioning version will be coppied in working_pulse_program.py

import csv
import crcmod
import matplotlib.pyplot as plt
import numpy as np

# Constants
TOTAL_BYTES = 512           # Max bytes per pulse
BYTE_TIME_NS = 0.2          # Each byte = 0.2ns
FIXED_WIDTH = 12            # Width of waveform in units (arbitrary)

a = 3/np.pi
VMAX = 1#VERY IMPORTANT FOR OPTICAL INTENSITY

def graph(num_points: int,
          func,
          output_csv: str,
          x_1fwhm,
          x_2fwhm,
          x_start,
          x_end,
          phi):
    x = np.linspace(x_start, x_end, num_points)
    y = func(x)
    #debug
    print("Minimum y / Maximum y =", y.min() / y.max())
    x = np.linspace(0,102.4, 512)
    y_norm = np.clip(np.floor((y / y.max()) * 255 * phi), 0, 255).astype(int)
    
    # Plot
    plt.plot(x, y_norm)
    plt.axhline(y=y_norm.max()/2, color='red', linestyle='--', linewidth=0.5, label='FWHM')
    plt.axvline(x=x_1fwhm,  color='red', linestyle='--', linewidth=0.5, label='FWHM')
    plt.axvline(x=x_2fwhm,  color='red', linestyle='--', linewidth=0.5, label='FWHM')
    #plt.title(name)
    plt.xlabel("Time (ns)")
    plt.ylabel("Amplitude (0-255)")
    plt.minorticks_on()

    # Major gridlines
    plt.grid(visible=True, which='major', linestyle='-', linewidth=0.8, color='gray')

    # Minor gridlines
    plt.grid(visible=True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')

    plt.show()
    #debug
    print("length of y_norm = ", len(y_norm))
    # Write to CSV
    if output_csv!=None:
        with open(output_csv, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(y_norm)
            print(f"Wrote {num_points} samples to {output_csv}")

def compute_crc_from_csv(csv_file: str):
    amplitude = bytearray()

    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            for val in row:
                try:
                    y_val = int(val.strip())
                    amplitude.append(y_val & 0xFF)
                    amplitude.append(0)  # 0-padding byte
                except ValueError:
                    print(f"Skipping invalid value: {val}")

    # CRC‑CCITT‑FALSE config
    crc_func = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    crc = crc_func(bytes(amplitude))

    print(f"CRC‑CCITT (0x1021, seed=0xFFFF): {hex(crc)}")    

def main():
    # Inputs
    t_pulse = int(input("Pulse duration - FWHM (ns): "))
    t_delay = int(input("Pulse delay (ns, max 102.4 - duration): "))
    IMAX = float(input("Maximum laser intensity, between 0 and 1 prefferably: "))
    period = TOTAL_BYTES * BYTE_TIME_NS
    ratio = FIXED_WIDTH / period
    eps = 1e-4
    #sigma is calculated in order to obtain the right FWHM width
    sigma = ratio * t_pulse / (np.sqrt(8 *np.log(2)))
    #we use sigma2 as a correction (without it, with only mu the pulse will only present the delay relative to the peak of the graph)
    sigma2 = t_pulse / (np.sqrt(4* np.log(1 / eps)))
    #debugging purpose calc
    print("sigma2 = ", sigma2)
    #
    mu = ratio * (((((((((((((((((((t_delay))))))))))))))))))) + sigma2
    phi = (0.5*a/VMAX)*np.arccos(0.5-IMAX)
    print("phi = ", phi)
    #just for debugging now
    x_1fwhm = (mu - sigma*np.sqrt(2*np.log(2)))/ratio
    x_2fwhm = (mu + sigma*np.sqrt(2*np.log(2)))/ratio
    print("width = ", (x_2fwhm-x_1fwhm))

    if ratio<0.5:
        mu = FIXED_WIDTH/2 - mu
    else:
        mu = mu - FIXED_WIDTH/2        

    height = 1 / (np.sqrt(2 * np.pi * sigma ** 2))

    def gauss(x):
        return height * np.exp(-((x + mu) ** 2) / (2 * sigma ** 2))
    
    def u(x):
        return a / (2*phi) * np.arccos(1 - 2 *  np.exp(-(x+mu)**2 / (2 * sigma ** 2)))
    
    def I_opt(x):
        return np.sin(phi* u(x) / a)**2


    output_csv = 'waveform.csv'
    graph(num_points=TOTAL_BYTES,
          func=gauss,
          output_csv= None,
          x_1fwhm = x_1fwhm,
          x_2fwhm = x_2fwhm,
          x_start=-FIXED_WIDTH / 2,
          x_end=+FIXED_WIDTH / 2,
          phi = 1)
    graph(num_points=TOTAL_BYTES,
          func=u,
          output_csv=output_csv,
          x_1fwhm = x_1fwhm,
          x_2fwhm = x_2fwhm,
          x_start=-FIXED_WIDTH / 2,
          x_end=+FIXED_WIDTH / 2,
          phi = phi)
    graph(num_points=TOTAL_BYTES,
          func=I_opt,
          output_csv=None,
          x_1fwhm = x_1fwhm,
          x_2fwhm = x_2fwhm,
          x_start=-FIXED_WIDTH / 2,
          x_end=+FIXED_WIDTH / 2,
          phi = 1)

if __name__ == '__main__':
    main()
