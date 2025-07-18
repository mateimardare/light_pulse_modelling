import csv
import crcmod
import matplotlib.pyplot as plt
import numpy as np

#TO IMPLEMENT!!!
#to introduce the tick 1 byte = 200ps for the ppg512
#to create the gaussian pulse aaaaaand
#to normalize it and translate it with an input value

# 512bytes * 200ps = 102.4ns
# t = input(int()) --> (as in pulse duration)
# start_offset = input(int()) --> what time to play after being triggered --> beforehand should eliminate 
# all the null values and rewrite the csv file

# it should also add the crc sum value at the end????

#maybe to make it more intuitive the input should be in time and the offset also

def graph(num_points: int,
          func,
          output_csv: str,
          x_start: float = -10.0,
          x_end: float = 10.0):
    x = np.linspace(x_start, x_end, num_points)
    y = func(x)

    max_y = y.max()

    # Normalize x to [0, 511]
    x_norm = (x - x_start) * (511 / (x_end - x_start))

    # Normalize y to [0, 511]
    y_norm = np.floor((y / max_y) * 255)

    y_norm = y_norm.astype(int)
    plt.plot(x_norm,y_norm)
    plt.show()
    y_hex = ['0x{:02X}'.format(val) for val in y_norm]



    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(y_norm)

    print(f"Wrote {num_points} samples to {output_csv}")


def compute_crc_from_csv(csv_file: str):
    amplitude = bytearray()

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        header_skipped = False
        for row in reader:
            if not header_skipped:
                header_skipped = True
                continue
            if len(row) < 2:
                continue
            try:
                y_value = int(row[1])  # y is the second column
                amplitude.append(y_value & 0xFF)
                amplitude.append(0)  # zero-padding byte
            except ValueError:
                print(f"Skipping invalid row: {row}")

    # CRC‑CCITT‑FALSE (poly=0x1021, init=0xFFFF, no-reflect, no-XORout)
    crc_func = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    crc = crc_func(bytes(amplitude))
    print(f"CRC‑CCITT (0x1021, seed=0xFFFF): {hex(crc)}")


def main():
    # Part 1: Generate Gaussian waveform
    sigma = 0.1
    height = 1/(np.sqrt(2*np.pi*sigma*sigma))

    def gauss(x):
        return height * np.exp(- (x ** 2) / (2 * sigma ** 2))

    output_csv = 'waveform.csv'
    graph(num_points=512,
          func=gauss,
          output_csv=output_csv,
          x_start=-4,
          x_end=+4)

    # Part 2: Compute CRC of y-values from waveform
    compute_crc_from_csv(output_csv)


if __name__ == '__main__':
    main()
