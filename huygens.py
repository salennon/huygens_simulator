'''
Classes to simulate wavelets of Huygens principle
'''

from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import os

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


    def animate(self, fig, ax, start, stop, time_step, filename):
        '''
        Simulate and generate animation over given timeframe between start 
        and stop with given time_step. 
        Animation is drawn on given figure and axis, and saved to filename

        TODO:
        Add clearer progress tracking
        Formatting of axes etc. - check these can be done externally to the 
        method
        '''
        time_points = np.arange(start, stop, time_step)
        im = ax.imshow(self.frame(time_points[0]), cmap = 'bwr')
        fig.colorbar(im)

        def generate_frame(i):
            '''Generate each frame of the animation using frame index i'''
            field = self.frame(time_points[i])
            print(i, time_points[i])
            im.set_array(field)
            return im,        #FuncAnimation requires iterable returned

        nframes = len(time_points)
        anim = FuncAnimation(fig, generate_frame, frames = nframes)
        anim.save(filename, fps = 60)

    # def simulate(self, start, stop, time_step, fig):
    #     '''
    #     Simulate fields between start and stop time, with given time step.
    #     '''
    #     time_points = np.arange(start, stop, time_step)

    #     for time in time_points:
    #         field = self.frame(time)







    def __str__(self):
        rep = f'Huygens simulator with {len(self.wavelets)} wavelet(s):'
        for wavelet in self.wavelets:
            rep += f'\n{wavelet.__str__()}'
        return rep
        


def main():
    '''
    TODO:
    Make clear individual test cases
    Optimise wavelet params, make sure that gif loops seamlessly.
    Centre the wavelet
    How to handle if simulation doesn't fit within z scale?
    '''
    

    ang_frequency = np.pi/5
    wave_vector = 2*np.pi/2
    pos = (5,5)

    wavelet = Wavelet(ang_frequency, wave_vector, pos)
    print(wavelet)
    
    wavelets = [wavelet]

    x = np.linspace(0, 20, 1000)
    y = np.linspace(0, 20, 1000)
    x_mesh, y_mesh = np.meshgrid(x, y)

    simulator = Simulator(wavelets, x_mesh, y_mesh)
    print(simulator)

    fig, ax = plt.subplots()
    start = 0.0
    stop = 10.0
    time_step = 0.25

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = f'{dir_path}/output/test.gif'
    simulator.animate(fig, ax, start, stop, time_step, filename)

    # field = simulator.frame(11)
    # # field = wavelet.field(11, x_mesh, y_mesh)
    # # plt.imshow(field)
    # # plt.show()

if __name__ == "__main__":
    main()



    