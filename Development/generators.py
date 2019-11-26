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

def cut(function, zlim=10.0 ,nanval=0):
	'''
	Handles NaNs and cuts z to ignore divergent parts of function.
	:Param function: The function to be tailored
	
	:Param zlim: Defines zmin and zmax constraint for function
	:Param nanval: Optional parameter, sets value to redefine NaNs as. 
	:Returns function: The function constrained between (-zlim < z < zlim with NaNs redefined.
	'''
	where_are_NaNs = isnan(function)
	function[where_are_NaNs] = nanval
	function[np.abs(function)>zlim] = zlim
	return function

def grid(lim=3, grid=4000):
	'''
	Sets up square mesh grid representing the xy plane.
	:Param lim: Sets up axes with |x| < lim and |y| < lim
	:Param grid: Side length of square array (grid x grid)
	:Returns: Tuple of meshed (X,Y) matrices for given limits
	'''
	x,y = np.linspace(-lim,lim,grid), np.linspace(-lim,lim,grid)
	return np.meshgrid(x,y)

def gamma(zlim=5, xylim=5):
	'''Calculates the gamma function in the complex xy-plane.'''
	X,Y = grid(lim=xylim)
	return np.abs(cut(sp.gamma(X+1.0j*Y),zlim=zlim))


def beta(zlim=10, xylim=3):
	'''Calculates the beta function for values in the real xy-plane.'''
	X,Y = grid(lim=xylim)
	return cut(sp.beta(X,Y),zlim=zlim)

def stripes(zlim=5, xylim=5):
	X,Y = grid(lim=xylim)
	return np.abs(cut(sp.gamma(X-Y),zlim=zlim))


def frame(array,fname ='fname',index = 0,cmap='Spectral'):
	#filepath to png
	filename = os.getcwd()+'/frames/{}_{}.png'.format(fname,index)
	#Get image
	print('Saving image')
	matplotlib.image.imsave(filename,array,cmap=cmap)
	print('Saved image to {} '.format(filename))
	input('--Enter--')

if __name__ =='__main__':


	gamma = gamma()
	beta = beta()
	stripes = stripes()

	frame(gamma,fname='g')
	frame(beta,fname='b')
	frame(stripes,fname='s')

