import matplotlib.pyplot as plt
import numpy as np

# Define constant a
a = 3 / np.pi
sigq = 1

def u(x: float | np.ndarray):
    return a / 2 * np.arccos(1 - 2 * np.exp(-x**2 / (2 * sigq)))

def du(x: float | np.ndarray):
    # Avoid invalid values due to sqrt of negative numbers
    with np.errstate(invalid='ignore'):
        return a * x / np.sqrt(np.exp(-x**2 / (2 * sigq)) - 1)

def main():
    x = np.linspace(-5, 5, 1000)
    y = u(x)
    dy = du(x)

    plt.plot(x, y, color='blue', label='u(x)')
    plt.plot(x, dy, color='red', label="u'(x)")

    plt.minorticks_on()

    plt.grid(visible=True, which='major', linestyle='-', linewidth=0.8, color='gray')
    plt.grid(visible=True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')

    plt.xlabel("x")
    plt.ylabel("Value")
    plt.title("Function u(x) and its Derivative")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
