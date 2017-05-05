#!/usr/bin/env/ python
"""Different methods for vortex detection
"""
import numpy as np

def calc_swirling(a):
    """
    2D Swirling strenght
    """
    print("Detection method: 2D swirling strenght")
    A = np.zeros((a.sizex*a.sizey,3,3))
    A = np.array([[a.derivative['dudx'].ravel(),a.derivative['dudy'].ravel(),
                a.derivative['dudz'].ravel()],[a.derivative['dvdx'].ravel(),
                a.derivative['dvdy'].ravel(),a.derivative['dvdz'].ravel()],
                [a.derivative['dwdx'].ravel(),a.derivative['dwdy'].ravel(),
                -a.derivative['dudx'].ravel()-a.derivative['dvdy'].ravel()]])

    A = A.transpose(2,1,0)
    eigenvalues = np.linalg.eigvals(A)
    swirling = np.max(eigenvalues.imag,axis=1).reshape(a.sizex,a.sizey)
    swirlMean = np.mean(swirling,axis=1)
    swirlingNorm = swirling/swirlMean[:,np.newaxis]
    where_are_NaNs = np.isnan(swirlingNorm)
    swirlingNorm[where_are_NaNs] = 0
    

    print(np.max(swirlingNorm))
    return swirling, swirlingNorm

def q_criterion(a):
    """
    Q Criterion
    vorticity magnitude and mean strain rate 
    """
    print("Detection method: Q criterion")
    Q = np.zeros((a.sizex,a.sizey))
    for i in range(a.sizex):
        for j in range(a.sizey):
            Q[i,j] = -0.5*(a.derivative['dudx'][i,j]**2
            + a.derivative['dvdy'][i,j]**2)
            - a.derivative['dudy'][i,j]*a.derivative['dvdx'][i,j]
    return Q
