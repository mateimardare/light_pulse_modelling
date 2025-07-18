#this script is mainly for testing 
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

def graph(num_points: int,
          func,
          output_csv: str,
          x_start: float = -10.0,
          x_end: float = 10.0):
    x = np.linspace(x_start, x_end, num_points)
    y = func(x)
    #debug
    print("Minimum y / Maximum y =", y.min() / y.max())

    y_norm = np.clip(np.floor((y / y.max()) * 255), 0, 255).astype(int)

    # Plot
    plt.plot(x, y_norm)
    plt.title("Normalized Gaussian Pulse")
    plt.xlabel("Time (arbitrary units)")
    plt.ylabel("Amplitude (0-255)")
    plt.grid(True)
    plt.show()
    #debug
    print("length of y_norm = ", len(y_norm))
    # Write to CSV
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
    t_pulse = int(input("Pulse duration (ns): "))
    t_delay = int(input("Pulse delay (ns, max 102.4 - duration): "))

    period = TOTAL_BYTES * BYTE_TIME_NS
    ratio = FIXED_WIDTH / period
    eps = 1e-4
    #mu needs recalculation
    mu = ratio * t_delay
    if ratio<0.5:
        mu = FIXED_WIDTH/2 - mu

    sigma = ratio * t_pulse / (2 * np.sqrt(np.log(1 / eps)))
    height = 1 / (np.sqrt(2 * np.pi * sigma ** 2))

    def gauss(x):
        return height * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    output_csv = 'waveform.csv'
    graph(num_points=TOTAL_BYTES,
          func=gauss,
          output_csv=output_csv,
          x_start=-FIXED_WIDTH / 2,
          x_end=+FIXED_WIDTH / 2)

    compute_crc_from_csv(output_csv)


if __name__ == '__main__':
    main()
