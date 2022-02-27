'''
Simulate diffraction from a single slit
'''

from huygens import Wavelet, Simulator
import numpy as np
import matplotlib.pyplot as plt
import os


def main():

    print('\nSingle slit simulation\n')

    #Wavelet parameters
    wavelength = 4.0
    period = 0.2
    ang_frequency = 2*np.pi/period
    wave_vector = 2*np.pi/wavelength

    #Wavelet positions
    x_pos = -50
    y_pos_min = -10
    y_pos_max = 10
    num_wavelets = 20
    positions = [(x_pos, y_pos) for y_pos in \
                 np.linspace(y_pos_min, y_pos_max, num_wavelets)]

    #Define wavelet(s) in simulation
    wavelets = [Wavelet(ang_frequency, wave_vector, position) for position in\
                 positions]

    #Simulation region
    x_min, x_max = -50, 50
    y_min, y_max = -50, 50
    x_res, y_res = 0.1, 0.1
    x = np.arange(x_min, x_max, x_res)
    y = np.arange(y_min, y_max, y_res)

    #Simulation time settings
    start = 0.0
    num_of_periods = 1                #Number of wavelet periods to record for
    time_steps_per_period = 30
    stop = start + num_of_periods*period
    time_step = period/time_steps_per_period

    #Initialize simulator
    simulator = Simulator(wavelets, x, y)
    print(simulator)

    #Generate simulation and animation
    fig, ax = plt.subplots()
    ax.set_title('Single slit')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = f'{dir_path}/output/single_slit.gif'
    simulator.animate(fig, ax, start, stop, time_step, filename)


if __name__ == "__main__":
    main()