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
        E(r,t) = A*cos[k*(r-r0) - wt + phi]

        Where:
        E is the field
        A is amplitude
        k is wave vector
        r is general position co-ordinate
        r0 is wavelet position
        w is angular frequency
        phi is phase
        r-r0 is the displacement vector from the wavelet

        The values of the field as a function of position are returned
        '''
        #Calculate displacement co-ords relative to wavelet location
        x_displacement = x_mesh - self.position[0]
        y_displacement = y_mesh - self.position[1]
        displacement = (x_displacement**2 + y_displacement**2)**0.5

        field = self.amplitude*np.cos(self.wave_vector*displacement - \
                self.ang_frequency*time + self.phase)

        return field


    def __str__(self):
        return f'Wavelet at co-ords {self.position}'


class Simulator():
    '''
    Handle simulation of given wavelets

    The simulation is a superposition (i.e. the sum) of the fields of all the 
    wavelets
    '''

    def __init__(self, wavelets, x, y):
        '''
        Init with a given list of wavelet objects
        x and y should be arrays to define simulation region
        '''
        self.wavelets = wavelets
        self.x = x
        self.y = y

        #Generate co-ordinate mesh
        self.x_mesh, self.y_mesh = np.meshgrid(x, y)
        assert self.x_mesh.shape == self.y_mesh.shape, \
                'X mesh and Y mesh should have the same shape'
        self.mesh_shape = self.x_mesh.shape


    def frame(self, time):
        '''Get frame of simulation at a given time point'''
        field = np.zeros(self.mesh_shape)

        #Sum contributions from each wavelet
        for wavelet in self.wavelets:
            field += wavelet.field(time, self.x_mesh, self.y_mesh)

        return field


    def animate(self, fig, ax, start, stop, time_step, filename):
        '''
        Simulate fields and generate animation over given timeframe between 
        start and stop with given time_step. 
        Animation is drawn on given figure and axis, and saved to filename

        TODO:
        Formatting of axes etc. - check these can be done externally to the 
        method
        '''
        time_points = np.arange(start, stop, time_step)

        #Use first frame to set z scale
        extent = (min(self.x), max(self.x), min(self.y), max(self.y))
        im = ax.imshow(self.frame(time_points[0]), cmap = 'RdBu', extent = extent,
                        origin = 'lower')
        
        #Formatting
        fig.colorbar(im)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        def generate_frame(i):
            '''Generate each frame of the animation using frame index i'''
            self.print_progress(i, num_frames)
            field = self.frame(time_points[i])
            im.set_array(field)
            return im,        #FuncAnimation requires iterable returned

        #Simulate + generate animation
        num_frames = len(time_points)
        print(f'\nGenerating Animation of {num_frames} frames.\nSimulating...\n')
        anim = FuncAnimation(fig, generate_frame, frames = num_frames)
        anim.save(filename, fps = 60)
        print(f'\nAnimation saved to {filename}\n')


    def simulate(self, start, stop, time_step):
        '''
        Simulate fields between start and stop time, with given time step.
        Results returned as a 3D array

        animate method is preferred at this point, which calculates each frame
        then, animates (so should require less memory usage)

        TODO:
        Test this method
        '''
        time_points = np.arange(start, stop, time_step)
        y_dim = self.mesh_shape[0]
        x_dim = self.mesh_shape[1]
        t_dim = len(time_points)
        result = np.empty((t_dim, y_dim, x_dim), dtype='float32')

        for i, time in enumerate(time_points):
            self.print_progress(i, t_dim)
            field = self.frame(time)
            result[i] = field
        
        return result


    @staticmethod
    def print_progress(i, num_frames, interval = 10):
        '''
        Print progress at given interval during simulation etc.
        i is the current frame index
        '''
        fr_num = i+1    #Convert from 0 indexed to 1
        if fr_num % interval == 0 or fr_num == num_frames:
            print(f'{fr_num}/{num_frames}')


    def __str__(self):
        rep = f'Huygens simulator with {len(self.wavelets)} wavelet(s):'
        for wavelet in self.wavelets:
            rep += f'\n{wavelet.__str__()}'
        return rep
        

def main():
    print('''
        huygens.py is a module containing classes to perform a 2D simulation of
        Huygens-Fresnel Principle - summing the contributions of multiple 
        spherical wavelets to generate a resultant wavefront

        Usage:
        Simulator instance handles the simulation - provide this with an
        iterable of wavelets (see Wavelet class) to be simulated, plus 
        simulation settings.
        Wavelet class handles each wavelet - initialize these first to be used
        by Simulator.

        ''')


if __name__ == '__main__':
    main()



    