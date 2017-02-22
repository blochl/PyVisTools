#!/usr/bin/env python3

import numpy as np
from math import ceil
import h5py
from PIL import Image
from os.path import splitext, getsize, isfile, join
from os import makedirs
import xml.etree.ElementTree as ET
from multiprocessing import Process
import sys

def to_u8(dat):
    dmin = dat.min()
    dmax = dat.max()
    if np.issubdtype(dat.dtype, np.uint8) and dmin == 0 and dmax == 255:
        return dat
    elif dmin != dmax:
        dat = ((dat - dmin) / (dmax - dmin)) * 255.0
    elif dmax:
        dat = (dat / dmax) * 255.0

    return dat.astype(np.uint8)


class pbar(object):
    def __init__(self, total):
        self.width = 50
        self.total = float(total)

    def advance(self, current):
        frac = current/self.total
        adv = int(ceil(frac * self.width))
        togo = self.width - adv
        perc = int(ceil(frac * 100))
        sys.stdout.write("\r[{0}] {1}%".format("#"*adv + "-"*togo, perc))
        sys.stdout.flush()

    def stop(self):
        sys.stdout.write("\n")


class export(object):
    def __init__(self, fname, dims='auto', divisor=64, write_tiffs=True):
        if not isfile(fname):
            print("File " + fname + " not found!")
            sys.exit(1)

        self.fname = fname
        self.dims = dims
        self.divisor = divisor
        self.write_tiffs = write_tiffs
        if self.dims == 'auto':
            try:
                xmlvals = ET.parse(self.fname + '.xml').getroot()
                for i in xmlvals.iter('SIZEZ'):
                    for j in xmlvals.iter('SIZEY'):
                        for k in xmlvals.iter('SIZEX'):
                            self.dims = [int(i.text), int(j.text), int(k.text)]
            except:
                print("Unable to determine dimensions from "
                      + self.fname + '.xml' + "\nPlease specify explicitly.\n"
                      "Format: [SIZEZ, SIZEY, SIZEX]")
                sys.exit(1)

    def get_bytelen(self, integer=False):
        bytelen, error = divmod(getsize(self.fname), np.prod(self.dims))
        if error:
            print("There is something wrong with the dimensions/filesize!")
            sys.exit(1)

        if bytelen == 1:
            self.dt = np.uint8

        if integer:
            if bytelen == 2:
                self.dt = np.uint16
            if bytelen == 4:
                self.dt = np.uint32
            if bytelen == 8:
                self.dt = np.uint64
        else:
            if bytelen == 2:
                self.dt = np.float16
            if bytelen == 4:
                self.dt = np.float32
            if bytelen == 8:
                self.dt = np.float64

        try:
            self.bytelen = np.dtype(self.dt).itemsize
            print("\033[92mDetected " + str(self.bytelen * 8) +
                  " bit data.\033[92m")
            print("\033[93mNote: assuming floating point, unless specified"
                  " as int!\033[0m")
        except NameError:
            print("Unsupported datatype!")
            sys.exit(1)

    def _get_framebunches(self):
        bunches, extra = divmod(self.dims[0], self.divisor)
        if bunches:
            self.fraclist = [bunches] * self.divisor
        else:
            self.fraclist = []

        if extra:
            self.fraclist.append(extra)

    def prep_files(self):
        self.h5file = h5py.File(splitext(self.fname)[0] + '.h5', 'w')
        self.h5ds = self.h5file.create_dataset("voldata", tuple(self.dims),
                                               compression="gzip",
                                               compression_opts=9,
                                               dtype=self.dt)
        if self.write_tiffs:
            print("\033[93mNote: .h5 => precise data; .tif => data is lost:"
                  " for visualization only!\033[0m")
            self.tiffdir = splitext(self.fname)[0] + '_8b_tiffs'
            makedirs(self.tiffdir, exist_ok=True)

    def _write_to_tiffs(self, i, m, frames):
        if self.write_tiffs:
            for j in range(m):
                im = Image.fromarray(to_u8(frames[j]))
                im.save(join(self.tiffdir, '{n:06d}.tif'.format(n=(j + m*i))),
                        compression="tiff_deflate")

    def write(self):
        if self.write_tiffs:
            print("Saving: " + splitext(self.fname)[0] +
                  '{.h5,_8b_tiffs/*.tif}')
        else:
            print("Saving: " + splitext(self.fname)[0] + '.h5')

        self._get_framebunches()
        pcount = 0
        p = pbar(len(self.fraclist))
        with open(self.fname, "rb") as f:
            for i, m in enumerate(self.fraclist):
                frames = f.read(m * np.prod(self.dims[1:]) * self.bytelen)
                frames = np.fromstring(frames, dtype=self.dt)
                frames = frames.reshape((m, self.dims[1], self.dims[2]))
                pwtf = Process(target=self._write_to_tiffs, args=(i, m, frames))
                pwtf.start()
                self.h5ds[i*m:(i+1)*m] = frames
                pwtf.join()
                p.advance(pcount)
                pcount += 1
            else:
                p.stop()

        self.h5file.close()

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print("Usage: " + sys.argv[0] + " <FILE>.vol")
        sys.exit(1)

    ex = export(fname, dims='auto', divisor=64, write_tiffs=True)
    ### Specified dimensions
    #dims = [2048, 2048, 2048]
    #ex = export(fname, dims = dims, divisor=64, write_tiffs=True)
    ex.get_bytelen(integer=False)
    ### For integer input data
    #ex.get_bytelen(integer=True)
    ex.prep_files()
    ex.write()
