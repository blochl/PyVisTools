# Script to export DF3 files from 3D NumPy arrays

This script allows to export density function (DF3) files from 3D NumPy arrays
for visualization in [POV-Ray](http://www.povray.org). This is useful for,
_e.g._, making high quality renderings of tomographic data. The array should be
read from an HDF5 file, although this can easily be changed.

## Prerequisits

* Python3
* NumPy
* h5py

## Usage

1. Set the following parameters inside the script:
  * `rdata`: path to the `.h5` file. [str]
  * `rdata_keys`: path to the desired dataset within the `h5` file. [list of str's]
  * `data_type`: Type of data for the desired output. DF3 supports only 8, 16, and 32 bits. [8|16|32]
  * `export_filename`: Path to the output file. [str]
2. Run the script.

## Licensing

Distributed under GPLv2.
