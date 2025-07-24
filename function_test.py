import numpy as np
import matplotlib.pyplot as plt

sigq = 1
ct1 = -0.3
ct2 = 1
def sa(x):
    return ct1*np.abs(x) + ct2*np.sin(x)/x

def func(x):
    return sa(x)+ np.exp(-x*x/(2*sigq))

def main():
    x = np.linspace(-7, 7, 1000)
    y = func(x)
    plt.plot(x, y)
    plt.minorticks_on()

    # Major gridlines
    plt.grid(visible=True, which='major', linestyle='-', linewidth=0.8, color='gray')

    # Minor gridlines
    plt.grid(visible=True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')

    plt.show()

if __name__=="__main__":
    main()