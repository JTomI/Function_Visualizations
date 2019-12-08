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
# from matplotlib.animation import FuncAnimation as animate

def cut(array, zlim=10.0 ,nanval=0):
	'''
	Handles NaNs and cuts z to ignore divergent parts of function.
	:Param function: The function to be tailored
	
	:Param zlim: Defines zmin and zmax constraint for function
	:Param nanval: Optional parameter, sets value to redefine NaNs as. 
	:Returns function: The function constrained between (-zlim < z < zlim with NaNs redefined.
	'''
	x,y = np.shape(array)
	array = array.flatten() #Flatten the original array so you can properly contruct truth array
	where_are_NaNs = isnan(array)
	array[where_are_NaNs] = nanval
	array[array>zlim] = zlim
	array[array<-zlim] = -zlim
	return array.reshape(x,y)

def grid(lim=3, grid=1500):
	'''
	Sets up square mesh grid representing the xy plane.
	:Param lim: Sets up axes with |x| < lim and |y| < lim
	:Param grid: Side length of square array (grid x grid).
	Optimal values is grid = 
	:Returns: Tuple of meshed (X,Y) matrices for given limits
	'''
	x,y = np.linspace(-lim,lim,grid), np.linspace(-lim,lim,grid)
	return np.meshgrid(x,y)

def gamma(xylim=5): # zlim = 5
	'''Calculates the gamma function in the complex xy-plane.'''
	X,Y = grid(lim=xylim)
	return np.abs(sp.gamma(X+1.0j*Y))

def beta(xylim=3): # zlim = 10
	'''Calculates the beta function for values in the real xy-plane.'''
	X,Y = grid(lim=xylim)
	return sp.beta(X,Y)

def stripes(xylim=5): # zlim = 5
	'''Calculates some interesting line contours of gamma function in the complex xy-plane.'''
	X,Y = grid(lim=xylim)
	return np.abs(sp.gamma(X-Y))

def waves(xylim=5):
	X,Y = grid(lim=xylim)
	return np.abs(sp.gamma(X-np.sin(Y)))

def tiles(xylim=5):
	X,Y = grid(lim=xylim)
	return np.abs(sp.gamma(np.cos(X)-np.sin(Y)))

def mask(xylim=5):
	X,Y = grid(lim=xylim)
	return np.abs(sp.gamma(np.cos(np.sinh(X))-np.sin(np.cosh(Y))))

def frame(array,fname ='fname',index = 0,cmap='Spectral'):
	'''
	Saves a .png of the provided array.
	:Param array: The numpy array to be converted to a .png.
	:Param fname: The name to be assigned to the .png file
	:Param index: Indexes the saved frame, so it is not overwitten 
	by later frames. Used when making a set of frames for movie.
	:Param cmap: The colormap to be applied to the image. Must be 
	chosen from matplotlib's colormap libraries.
	'''
	filename = os.getcwd()+'/frames/{}_{}.png'.format(fname,index)
	matplotlib.image.imsave(filename,array,cmap=cmap)

def gen_frames(function,zlims,fname ='fname',cmap='Spectral'):
	array = function()
	print('Generating Frames')
	for i in tqdm(range(zlims.size)):
		cutarray = cut(array,zlim=zlims[i])
		frame(cutarray,fname=fname,index=i,cmap=cmap)

def stitch(function, zlims, fname='fname', cmap='Spectral', off=0, fps=20):
	'''Uses the ffmpeg terminal command to stitch together the png frames into a .mp4 movie file with given fps. Offset counter to adjust for cache'''
	# directs to frames to be iterated over. %d is interpreted by ffmpeg along with -start_number
	# this %d allows ffmpeg to iterated over sequential files in the /frames folder, and make a movie
	gen_frames(function,zlims,fname=fname,cmap=cmap) # make frames at given fps
	input(' :: Check /frames to see generated frames :: \n :: Press <Enter> to Continue :: ')
	cwd = os.getcwd()
	location = cwd + '/frames/{}_%d.png'.format(fname) 
	# command output will be mp4 file at given fps. Suppress command line output (verbose command)
	ffmpeg_cmd = "ffmpeg -r {} -start_number {} -i {} -vcodec mpeg4 {}.mp4".format(fps , off , location , fname)
	os.system(ffmpeg_cmd) # make the movie
	os.system('rm -R frames') # cleanup frames folder. --Maybe make this file specific?
	os.system('mkdir frames') # cleanup frames folder
	savemsg = ' :: {}.mp4 saved in {} :: '.format(fname , cwd)
	return(savemsg)


if __name__ =='__main__':
	# zlims = np.linspace(.01,10,200)
	# msg = stitch(test,zlims,fname='test',fps=10)
	# print(msg)
	g = 50
	X,Y = grid(grid = g)
	function = test(g = g)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1,projection ='3d')
	vis = ax.plot_trisurf(X.flatten(),Y.flatten(),function.flatten(),cmap=plt.cm.CMRmap)
	fig.colorbar(vis, shrink=0.5, aspect=5)
	fig.show()
	input('__Enter__')

