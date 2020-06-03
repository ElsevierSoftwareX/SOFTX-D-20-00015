#!/usr/bin/env/ python
"""
Convert ASCII files to NetCDF4 (plain text)
"""
from netCDF4 import Dataset
import argparse
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert file from ASCII to netCDF format',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input', dest='infile',
                        help='input ASCII file', metavar='FILE')

    parser.add_argument('-o', '--output', dest='outfile',
                        help='output NetCDF file', metavar='FILE')

    args = parser.parse_args()


grp1 = Dataset(args.outfile, 'w', format='NETCDF4')
grp1.description = 'Experiments conducted at Rouen ...'

ndimx = 159 # spacing
ndimy = 134 # spacing

# dimensions
grp1.createDimension('resolution_x', ndimx)
grp1.createDimension('resolution_y', ndimy)
grp1.createDimension('resolution_z', 1)

# variables
velocity_x = grp1.createVariable('velocity_x', 'f4', ('resolution_z',
                                                      'resolution_y',
                                                      'resolution_x'))
velocity_y = grp1.createVariable('velocity_y', 'f4', ('resolution_z',
                                                      'resolution_y',
                                                      'resolution_x'))
velocity_z = grp1.createVariable('velocity_z', 'f4', ('resolution_z',
                                                      'resolution_y',
                                                      'resolution_x'))
grid_x = grp1.createVariable('grid_x', 'f4', 'resolution_x')
grid_y = grp1.createVariable('grid_y', 'f4', 'resolution_y')

# data
#velocity_x[:] = np.random.random((1,ndimy,ndimx))/1
#velocity_y[:] = np.random.random((1,ndimy,ndimx))/1
#velocity_z[:] = np.random.random((1,ndimy,ndimx))/1

# grid
x = np.linspace(0, ndimy, ndimx)
y = np.linspace(0, ndimy, ndimx)

infile = open(args.infile, 'r')
line=infile.readline()
lines = infile.readlines()
for j in range(ndimy):
    for i in range(ndimx):
        velocity_x[0, j, i] = lines[j*ndimx+i].split()[2]
        velocity_y[0, j, i] = lines[j*ndimx+i].split()[3]
        if j == 0:
            grid_x[i] = lines[i].split()[0]
        if i == 0:
            grid_y[j] = lines[j*ndimx].split()[1]

grp1.close()
