# Convert a raw data volume to a compressed HDF5 \& 8-bit tiffs

This allows to convert a raw 3D data to a strongly compressed HDF5 file, and,
optionally, to a series of 8-bit tiff images.

There is a balance between memory usage and the speed of operation. You can
set the `divisor` parameter ([1..N-frames]) to a lower value for faster
operation and more memory usage, or to a higher value for smaller memory
footprint and slower operation. The default value is 64, which results in less
than 3 GB RAM usage with 2048x2048x2048 32-bit dataset, and approx. 30 min.
run time.

If the raw data is of more than 8-bit depth, data loss occurs during the tiff
conversion. Thus, for such data the tiff format should be used for
visualization purposes only, and not for quantitative analysis. The full
precision is obviously always preserved in the HDF5 file.

This script relies on the presence of an xml file, **FILENAME.vol.xml**, to
determine the volume dimensions. It is usually present if the volume was
constructed at the [ESRF](http://www.esrf.eu). Otherwise - just specify
the dimensions in the script.

The data is assumed to be floating point values. If the data are integers,
change the `integer` argument to `True` in the end of the script. (Or just
uncomment the ready-made line, and comment the default one.)

## Prerequisits

* Python3
* NumPy
* h5py
* Pillow
* Libtiff installed

## Usage

* For standard ESRF vol data, just run:
  ```
  ./volconv.py /path/to/data.vol
  ```

* For other cases, just make sure to set the `dims` and `integer` arguments
  right (in the end of the script). And do the same as above.

* You can also reduce the `divisor` argument, for faster (yet more memory
  intensive) operation, and set `write_tiffs` to `False` if you don't want
  tiff images of the dataset.

## Licensing

Distributed under GPLv2. You can find the full license text [here](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
