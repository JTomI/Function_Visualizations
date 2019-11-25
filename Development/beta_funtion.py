import numpy as np
import matplotlib
import os
import matplotlib.pyplot as plt
from scipy import special as sp
from scipy.integrate import quad
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm


def paint(cm='gray', color_map =[1,0,1,0,1,0], grad=False):
	'''Generates the pal colormap values to be used in scipy.misc.toimage. Defaults are stored in self.colordict, and are called by their names in new instance'''
	colordict = {'fiery':[1/3,150,1,0,1/6,0],'blue':[1/6,0,0,20,1,0],'xmas':[-1/1.5,160,1,0,0.2,0],'70s':[.5,255/2,-1,255,-1,255],'gray':[1,0,1,0,1,0],'teal':[0,0,1,0,1,0],'poison':[1,0,0,30,0,200],'misc':[-1/1.5,150,1,0,0.5,70]}
	if grad:
		m1, b1, m2, b2, m3, b3 = color_map
		triplet = [[0,0,0]]
		for i in range(1,255):
			triplet.append([m1*i+b1 , m2*i+b2 , m3*i+b3])
		return(triplet)
	else:
		try:
			cm = str(cm)
			assert cm in colordict
		except Exception:
			print('''Invalid colormap, available choices: \n \n {}'''.format(colordict))
		else:
			m1, b1, m2, b2, m3, b3 = colordict[cm]
			triplet = [[0,0,0]]
			for i in range(1,255):
				triplet.append([m1*i+b1 , m2*i+b2 , m3*i+b3])
			return(triplet)

def bcut(beta,grid, zlim =10.0):
	'''cuts z to remove divergent parts of function.'''
	beta = beta.flatten()
	for i in range(beta.size):
		if beta[i] > zlim:
			beta[i] = zlim
		if beta[i] < -zlim:
			beta[i] = -zlim
	return beta.reshape((grid,grid))

def beta_int(t,x,y):
	'''Beta function integrand'''
	return t**(x-1)*(1-t)**(y-1)

def beta_brute(x,y,grid):
	'''Calculation of beta function from brute force integration'''
	x,y = x.flatten(), y.flatten()
	beta,error = np.zeros_like(x),np.zeros_like(x)
	for i in tqdm(range(beta.size)):
		beta[i], error[i] = quad(beta_int,0,10,args=(x[i],y[i]))
	return beta.reshape((grid,grid)) 


if __name__ =='__main__':
	# print(sp.beta.__doc__)
	index = 0
	name = 'grid_1{}_1000'.format(index)
	# cmap = plt.cm.CMRmap
	cmap = 'coolwarm'
	lim = 3; grid =30; #No point going beyond 4k 
	print('Setting up axes')
	x,y = np.linspace(-lim,lim,grid), np.linspace(-lim,lim,grid)
	print('Setting up meshgrid')
	X,Y = np.meshgrid(x,y)
	print('Calculating Beta')
	beta = bcut(sp.beta(X,Y),grid)

	#====================================================================================
	#Save as png image (cool AND handles a large grid size)
	#====================================================================================
	# print('Saving image')
	# matplotlib.image.imsave(os.getcwd()+'/frames/{}.png'.format(name),beta,cmap=cmap)
	# input('--Enter--')

	#====================================================================================
	#Tri - Surface plot (cool but can only handle a small grid)
	#====================================================================================
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1,projection ='3d')
	vis = ax.plot_trisurf(X.flatten(),Y.flatten(),beta.flatten(),cmap=plt.cm.CMRmap)
	fig.colorbar(vis, shrink=0.5, aspect=5)

	fig.show()
	input('--Enter--')
# 
	#====================================================================================
	#2D Contour plot (ugly and only handles a small grid)
	#====================================================================================

	# fig,ax = plt.subplots(1,1)
	# ax.set_title('Beta Function')
	# cp = ax.contourf(X, Y, beta)
	# ax.set_xlabel('x'),ax.set_ylabel('y')
	# fig.colorbar(cp, title ='B(x,y)') # Add a colorbar to a plot

	# fig.show()
	# input('--Enter--')


