'''
Testing matplotlib animation using imshow
'''

from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import os


def main():
    '''
    Test matplotlib animation with random data
    '''
    fig, ax = plt.subplots()
    time_points = np.arange(0, 10, 0.25)
    im = ax.imshow(np.random.rand(10,10))

    def generate_frame(i):
        field = np.random.rand(10,10)
        im.set_array(field)
        return [im]        #FuncAnimation requires iterable returned

    anim = FuncAnimation(fig, generate_frame,
                            frames = len(time_points))
                        
    dir_path = os.path.dirname(os.path.realpath(__file__))
    anim.save(f'{dir_path}/test_output/test.gif')


if __name__ == "__main__":
    main()