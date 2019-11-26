import numpy as np
from numpy import *
import matplotlib
import os
import matplotlib.pyplot as plt
from scipy import special as sp
from scipy.integrate import quad
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
from matplotlib.animation import FuncAnimation as animate

def cut(gamma,grid, zlim =10.0):
	'''Handles NaNs and cuts z to ignore divergent parts of function.'''
	where_are_NaNs = isnan(gamma)
	gamma[where_are_NaNs] = 0
	gamma[np.abs(gamma)>zlim] = zlim
	return gamma
	
def xsection(gamma, grid,zlim):
	return np.abs(cut(gamma,grid,zlim=zlim))


def frame(lim=5,grid=4000,index = 0,cmap='Spectral'):
	#filepath to png
	filename = os.getcwd()+'/frames/gamma_{}.png'.format(index)
	#define grid and do math
	x,y = np.linspace(-lim,lim,grid), np.linspace(-lim,lim,grid) #(Multiply y by 1.0j to get line structure)
	X,Y = np.meshgrid(x,y)
	gamma = xsection(sp.gamma(X+1.0j*Y), grid,zlim = lim)
	#Get image
	print('Saving image')
	matplotlib.image.imsave(filename,gamma,cmap=cmap)
	print('Saved image to {} '.format(filename))
	input('--Enter--')


if __name__ =='__main__':
	frame()




