Python simulator for Huygens' Principle in 2D

Huygens' Principle is a model used to explain phenomena of propagating light,
such as diffraction. The Principle states that each point on a wavefront can be
regarded as a source of spherical wavelets (points which emit a spherical 
wavefront). The sum of these spherical wavelets forms the resulting wavefront.

This simulator allows the user to specify the locations of the spherical
wavelets and simulate the resulting wavefront. At each time step of the
simulation, the field from each wavelet is calculated analytically and the 
contributions from the wavelts are summed to give the resultant wavefront.
Computation is performed using numpy arrays for efficiency and animations are
generated with Matplotlib.

-----

Usage:
Most modules and scripts are contained in the huygens_simulator directory.

huygens.py contains the classes used for simulation - import this into your
script and use the Wavelet class to specify each spherical wavelet, then an
instance of the Simulator class to run the simulation.

See scripts in huygens_simulator for example usage:

single_wavelet.py - Simulation of a single wavelet
wavefront.py - Simulation of a row of wavelets to simulate a propagating plane
wave.

Output animations from these simulations can be found in:
huygens_simulator/output
