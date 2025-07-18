import csv
import crcmod
import matplotlib.pyplot as plt
import numpy as np

TICK_PS = 200  # 200 picoseconds per byte
BYTES_PER_NS = 1000 / TICK_PS  # 5 bytes = 1 ns

def graph(duration_ns: int,
          offset_ns: int,
          func,
          output_csv: str,
          x_start: float = -4,
          x_end: float = 4):

    total_bytes = duration_ns * BYTES_PER_NS
    offset_bytes = offset_ns * BYTES_PER_NS

    x = np.linspace(x_start, x_end, 512)
    y = func(x)

    max_y = y.max()
    if max_y == 0:
        raise ValueError("Function returned all zeros. Cannot normalize.")
    y_norm = np.floor((y / max_y) * 255)

    y_norm = y_norm.astype(int)


    print("Non-zero normalized samples:")
    print(y_norm)
    print("Offset (in bytes):", offset_bytes)

    # Apply offset
    z = [0] * offset_bytes
    z.extend(y_norm.tolist())  # ensure y_norm is flattened if needed

    print("Waveform after offset but before padding:")
    print(np.array(z)[np.array(z) != 0])

    # Ensure exactly 512 bytes
    z = z[:512]
    while len(z) < 512:
        z.append(0)

    z = np.array(z, dtype=int)

    # Plot the waveform
    plt.plot(np.arange(len(z)), z)
    plt.title("Gaussian Pulse with Offset")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

    # Save to CSV as stringified decimals
    with open(output_csv, 'w', newline='') as f:
        f.write(';'.join(map(str, z)))

    print(f"Wrote waveform of {len(z)} bytes to {output_csv}")

    return z

def compute_and_append_crc(data: np.ndarray, output_file: str):
    amplitude = bytearray()
    for val in data:
        amplitude.append(val & 0xFF)
        amplitude.append(0)  # zero-padding

    # Compute CRC‑CCITT‑FALSE
    crc_func = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    crc = crc_func(bytes(amplitude))
    print(f"CRC‑CCITT (0x1021, seed=0xFFFF): {hex(crc)}")

    # Append CRC to file
    with open(output_file, 'a') as f:
        f.write(f";CRC=0x{crc:04X}\n")


def main():
    # Inputs
    duration_ns = int(input("Enter pulse duration (in ns): "))  # e.g., 100
    offset_ns = int(input("Enter start offset (in ns): "))      # e.g., 2

    sigma = 0.1
    height = 1 / (np.sqrt(2 * np.pi * sigma ** 2))

    def gauss(x):
        return height * np.exp(- (x ** 2) / (2 * sigma ** 2))

    output_csv = 'waveform.csv'
    y_data = graph(duration_ns, offset_ns, gauss, output_csv)
    compute_and_append_crc(y_data, output_csv)


if __name__ == '__main__':
    main()
