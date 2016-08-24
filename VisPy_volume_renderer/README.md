# Volume rendering using VisPy

This script allows to render volumes contained within NumPy arrays, in an HDF5
file. Also, the threshold for isosurface can be changed interactively - a
helpful visual aid for determining the threshold value.

## Prerequisits

* Python3
* VisPy
* h5py
* PyOpenGL

## Usage

1. Set the following parameters inside the script:
  * `rdata`: path to the `.h5` file. [str]
  * `rdata_keys`: path to the desired dataset within the `h5` file. [list of str's]
  * `z_stretch`: Stretch factor for displaying the **z** direction (in many cases the vertical direction requires different scaling). [float]
  * `thresh_delta`: The increment by which the threshold for isosurface is interactively increased/decreased. [float]
2. Run the script. The interaction instructions will be shown in the terminal window.

## Troubleshooting

* Notice that the _Fly_ camera mode has different controls (as shown upon starting the script). Navigating using the mouse wheel in _Fly_ mode will cause errors (which can be safely ignored).
* If you do not see the display window, or errors appear, please make sure that the dependencies are installed correctly, or install any additional dependencies, as needed.

## Credits

* Based on the work of [Vispy Development Team](http://vispy.org).
* Distributed under the (new) BSD License.
