import matplotlib.pyplot as plt
import numpy as np

# Define constants
a = 3 / np.pi
sigq = 1
CT = np.linspace(0.1, 1, 10) #this ct value actually gives the maximum optical intensity that shall be reached

def u(x: float | np.ndarray, ct: float):
    return a / 2 * np.arccos(1 - 2 * ct * np.exp(-x**2 / (2 * sigq)))

def I_opt(u_func, x, ct):
    return np.sin(u_func(x, ct) / a)**2

def main():
    x = np.linspace(-5, 5, 1000)
    y = []
    y_opt = []

    # First Plot: u(x)
    plt.figure(figsize=(10, 5))
    for ct in CT:
        y_val = u(x, ct)
        y.append(y_val)
        plt.plot(x, y_val, linestyle='-', label=f'u(x) for ct={ct:.2f}')
    
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.title("u(x) for varying ct values")
    plt.grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
    plt.grid(True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')
    plt.minorticks_on()
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Second Plot: I_opt(x)
    plt.figure(figsize=(10, 5))
    for ct in CT:
        y_optval = I_opt(u, x, ct)
        y_opt.append(y_optval)
        plt.plot(x, y_optval, linestyle='--', label=f'I_opt(x) for ct={ct:.2f}')
    
    plt.xlabel("x")
    plt.ylabel("I_opt(x)")
    plt.title("I_opt(x) for varying ct values")
    plt.grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
    plt.grid(True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')
    plt.minorticks_on()
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
