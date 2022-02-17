'''
Classes to simulate wavelets of Huygens principle
'''

import numpy as np
import matplotlib.pyplot as plt

class Wavelet():
    '''
    Represent a single wavelet of Huygens' principle
    '''
    def __init__(self, ang_frequency, wave_vector, 
                position, amplitude = 1.0, phase = 0.0):
        self.ang_frequency = ang_frequency
        self.wave_vector = wave_vector
        self.phase = phase
        self.amplitude = amplitude
        self.position = position

    def calculate_field(self, time, x_mesh, y_mesh):
        '''
        Calculate field from wavelet at given time using given x and y 
        co-ordinates in x_mesh and y_mesh arrays.

        Field is calculated according to:
        A*exp(j*[k*(r-r0) - wt + phi])

        Where:
        A is amplitude
        j is the imaginary unit (-1**0.5)
        k is wave vector
        r is general position co-ordinate
        r0 is wavelet position
        w is angular frequency
        phi is phase
        r-r0 is the displacement vector from the wavelet

        Real value of field is returned (corresponds to physical situation)
        '''

        x_displacement = x_mesh - self.position[0]
        y_displacement = y_mesh - self.position[1]
        displacement = (x_displacement**2 + y_displacement**2)**0.5

        field = self.amplitude*np.exp(1j*(self.wave_vector*displacement - \
                self.ang_frequency*time + self.phase))

        return field.real




def main():
    wavelet = Wavelet(2*np.pi/2, 2*np.pi/2, (5,5))

    x = np.linspace(0, 10, 1000)
    y = np.linspace(0, 10, 1000)
    x_mesh, y_mesh = np.meshgrid(x, y)

    field = wavelet.calculate_field(11, x_mesh, y_mesh)
    plt.imshow(field)
    plt.show()

if __name__ == "__main__":
    main()



    