#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Written by Leonid Bloch (c) 2016
# Distributed under GPLv2
# -----------------------------------------------------------------------------

import sys
import numpy as np
import h5py

### CHANGE THESE ###
rdata = 'trydata.h5'
rdata_keys = ['labels']
data_type = 8 # Only 8, 16, and 32 are supported!
export_filename = 'trydata.df3'
###################

class np2df3(object):
    def __init__(self, arr, dt, outname):
        self.arr = arr
        self.origsize = np.array(self.arr.shape)
        self.outname = outname
        self.dt = dt
        if self.dt == 8:
            self.t = 'u1'
        elif self.dt == 16:
            self.t = '>u2'
        elif self.dt == 32:
            self.t = '>u4'
        else:
            print("Error! Please request a data type only in [8|16|32]!")
            sys.exit(1)

    def check_dim(self):
        if self.origsize.shape[0] != 3:
            print("Error! Only 3 dimensional arrays are supported!")
            sys.exit(1)
        elif self.origsize.max() > 65533:
            print("Error! The array is too large!")  # Upto 2**16-3
            sys.exit(1)

    def norm_arr(self):
        '''
        Makes normalized array of type float64
        '''
        try:
            self.arr.astype(np.float64)
        except:
            print("Error! Please check your array!")
            sys.exit(1)

        _minval = self.arr.min()
        _maxval = self.arr.max()
        if _minval == _maxval:
            self.arr /= _maxval
        else:
            self.arr = (self.arr - _minval)/(_maxval - _minval)

    def pad_arr(self):
        '''
        Pads array with zeros on each dimension to take care of edge effects
        '''
        self.padded_size = self.origsize + 2
        self.pad = np.zeros(self.padded_size)
        self.pad[1:-1, 1:-1, 1:-1] = self.arr

    def to_dt(self):
        '''
        Transforms the normalized, padded array to the desired data type, with
        values that use the entire range of that data type.
        '''
        _maxval = 2**self.dt - 1
        self.pad = (self.pad * _maxval).astype(self.t)

    def export(self):
        self.check_dim()
        self.norm_arr()
        self.pad_arr()
        self.to_dt()
        with open(self.outname, 'wb') as f:
            self.padded_size[::-1].astype('>u2').tofile(f)
            self.pad.tofile(f)


if __name__ == '__main__':
    with h5py.File(rdata, 'r') as hf:
        for k in rdata_keys:
            vol = hf[k]
        else:
            vol = vol.value

    np2df3(vol, data_type, export_filename).export()
