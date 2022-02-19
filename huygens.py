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


    def field(self, time, x_mesh, y_mesh):
        '''
        Calculate field from wavelet at given time using given x and y 
        co-ordinates in x_mesh and y_mesh arrays.

        Field is calculated according to:
        E(r,t) = A*exp(j*[k*(r-r0) - wt + phi])

        Where:
        E is the field
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
        #Calculate displacement co-ords relative to wavelet location
        x_displacement = x_mesh - self.position[0]
        y_displacement = y_mesh - self.position[1]
        displacement = (x_displacement**2 + y_displacement**2)**0.5

        field = self.amplitude*np.exp(1j*(self.wave_vector*displacement - \
                self.ang_frequency*time + self.phase))

        return field.real


    def __str__(self):
        return f'Wavelet at co-ords {self.position}'


class Simulator():
    '''
    Handle simulation of given wavelets
    '''

    def __init__(self, wavelets, x_mesh, y_mesh):
        '''
        Init with a given list of wavelet objects
        x_mesh and y_mesh define simulation region
        '''
        self.wavelets = wavelets

        assert x_mesh.shape == y_mesh.shape, \
            "x mesh and y mesh must have the same shape"
        self.x_mesh = x_mesh
        self.y_mesh = y_mesh
        self.mesh_shape = x_mesh.shape


    def frame(self, time):
        '''Get frame of simulation at a given time point'''
        field = np.zeros(self.mesh_shape)

        #Sum contributions from each wavelet
        for wavelet in self.wavelets:
            field += wavelet.field(time, self.x_mesh, self.y_mesh)

        return field   


    def __str__(self):
        rep = f'Huygens simulator with {len(self.wavelets)} wavelet(s):'
        for wavelet in self.wavelets:
            rep += f'\n{wavelet.__str__()}'
        return rep
        




def main():
    ang_frequency = 2*np.pi/2
    wave_vector = 2*np.pi/2

    wavelet = Wavelet(2*np.pi/2, 2*np.pi/2, (5,5))
    print(wavelet)
    
    wavelets = [wavelet]

    x = np.linspace(0, 10, 1000)
    y = np.linspace(0, 10, 1000)
    x_mesh, y_mesh = np.meshgrid(x, y)

    simulator = Simulator(wavelets, x_mesh, y_mesh)
    print(simulator)


    field = simulator.frame(11)
    # field = wavelet.field(11, x_mesh, y_mesh)
    plt.imshow(field)
    plt.show()

if __name__ == "__main__":
    main()



    