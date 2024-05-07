#!/usr/bin/env python

import numpy as np
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.utility.Swq import *
import itertools

lat_type = 'triangular'
#lat_type = 'honeycomb'

latt_uc,sites_uc = build_latt(lat_type,2,2,1,return_neigh=False)
sites_cart_uc = np.dot(sites_uc,latt_uc)


nx=30
ny=30
latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False)
nat = sites.shape[2]
sites_cart = np.dot(sites,latt)

quiver_kws = dict(
scale=2,
units='x',pivot='mid')
 
spin_plot_kws=dict(
scatter_size=10,
quiver_kws=quiver_kws,
colorful_quiver=False,
#superlatt=np.dot(np.diag([nx,ny]),latt),
superlatt=np.dot(np.diag([2,2]),latt),
#facecolor='k',
)

cbar_kws=dict(
colorbar_axes_position=[0.75,0.5,0.02,0.25],
colorbar_orientation='vertical',
#colorbar_shrink=0.5,
)


BZ = np.array([[1/3,1/3],[-1/3,2/3],[-2/3,1/3],[-1/3,-1/3],[1/3,-2/3],[2/3,-1/3],[1/3,1/3]])
BZ_2nd = np.array([[1,0],[0,1],[-1,1],[-1,0],[0,-1],[1,-1],[1,0]])

rcell = 2*np.pi*np.linalg.inv(latt).T
BZ_cart = np.dot(BZ,rcell)
BZ_2nd_cart = np.dot(BZ_2nd,rcell)


all_confs = [
#'FM',
#'Neel',
#'Zigzag',
#'Stripy',
#'super-Neel',
'Tetrahedra',
#'Cubic',
]


nqx=120
nqy=120
qpt_cart = gen_uniform_qmesh(nqx,nqy,bound=11)
 

sf_kws = dict(
scatter_size=10,
nqx=nqx,
nqy=nqy,
nn=3,
colormap='hot',
)

 
if __name__=='__main__':
    for conf_name in all_confs:
        sp_lat_uc, latt, sites_muc = regular_order(lat_type,conf_name)
        #sites_cart = np.dot(sites_muc, latt)

        #sp_lat_uc = np.roll(sp_lat_uc,axis=0,shift=1)

        sp_lat = np.zeros((nx,ny,nat,3))

        rx=range(0,nx,2)
        ry=range(0,ny,2)
        for i,j in itertools.product(rx,ry):
            sp_lat[i:i+2,j:j+2] = sp_lat_uc

        Q=calc_topo_chg(sp_lat,sites_cart)
        title = '{} order'.format(conf_name)
        #title += ', Q = {:10.5f}'.format(Q)
        spin_plot_kws.update(title=title)
        if conf_name in ['Tetrahedra','Cubic']:  
            spin_plot_kws.update(colorful_quiver=True)

        spins = sp_lat.reshape(-1,3)
        S_vector = calc_static_structure_factor(spins,sites_cart.reshape(-1,2),qpt_cart)
        #S_vector = calc_static_structure_factor_new(sp_lat,latt,sites,qpt_cart)
        #S_vector = pickle.load(open('S_vector.pickle','rb'))

        fig,ax = plt.subplot_mosaic([['a','a'],['b','c']])
        #scat, qv, tl = ax_plot_spin_2d(ax['a'],sites_cart,sp_lat,**spin_plot_kws)
        scat,qv,tl = ax_plot_spin_2d(ax['a'],sites_cart_uc,sp_lat_uc,**spin_plot_kws)
        axi = ax['a'].inset_axes([1.1,0.1,0.05,0.5])
        fig.colorbar(scat,cax=axi)
        axi.set_title('$n_z$')

        subplot_struct_factor(ax['b'],qpt_cart,S_vector,comp='parall',**sf_kws)
        subplot_struct_factor(ax['c'],qpt_cart,S_vector,comp='normal',**sf_kws)
        for key in ['b','c']:
            ax[key].plot(BZ_cart[:,0],BZ_cart[:,1],'w--',zorder=1,alpha=0.4)
            ax[key].plot(BZ_2nd_cart[:,0],BZ_2nd_cart[:,1],'w--',zorder=1,alpha=0.4)

        fig.tight_layout()
        plt.show()

