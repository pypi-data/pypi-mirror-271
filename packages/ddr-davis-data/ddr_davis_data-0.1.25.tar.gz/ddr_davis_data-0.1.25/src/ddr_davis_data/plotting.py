# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 21:04:55 2022

@author: darsh
"""

import matplotlib as _mpl
import matplotlib.pyplot as _plt
import numpy as _np
import pandas as _pd


def remove_ax_lines(ax):
    for spine in ['top', 'right','bottom','left']:
        ax.spines[spine].set_visible(False)
    return ax

# def plot_quiver(vel_set=None,n=0,data=None,ax=None,fracx=6,fracy=None,scale=0.8,width=0.1,headwidth=12,headlength=15,minshaft=2,minlength=0.1,units='xy',scale_units='xy'):
def plot_quiver(vel_set=None,n=0,data=None,ax=None,fracx=3,fracy=None,scale=50,width=0.0015,headwidth=4,normalize=True,**kwargs):
    '''
    plots quiver (vectors) either from vel_set or data, whichever is defined. If vel_set is defined then n (image number), 'z'(saclar to plot) is to be
    defined. If both vel_set and data are defined then data is given the priority above vel_set.

    Parameters
    ----------
    vel_set : velocity_set, optional
        either provide the velocity set or the data for plotting. The default is None.
    n : int, optional
        image/frame number. This is used when vel_set is supplied to the function. If data is directly given then this option is not useful. The default is 0.
    data : dict, optional
        dictionary-like object containing 'x','y',and 'z' keys and numpy_masked array like values. The 'z' values are contour filled in 'x' and 'y' coordinates.
        This is optional if the vel_set is defined. The default is None.
    ax : matplotlib.pyplot.axes like, optional
        axes on which to plot. The default is None. If not specified then plt.gca() is used for plotting.
    fracx : int, optional
        sub-sample over the x-axis to reduce the clutter. If fracx is 4 then for every 4 data one will be taken for plotting. The default is 3.
    fracy : str or int, optional
        Same as fracx but in y-direction. The default is None. If None then fracy = fracx
    normalize : bool, optional
        whether to normalize the vector for plotting. if true, vectors are normalized with its magnitude. make this true if vectors vary too much in magnitude over the plot.
    **kwargs : plt.quiver keyword arguments
        gives the freedom to modify the plot according to the needs.

    Returns
    -------
    ax : matplotlib.pyplot.axes like
        returns the axes with plot

    '''
    if ax is None:
        ax = _plt.gca()
    
    if data is None:
        data = vel_set.make_data(n=n)
    
    if fracy is None:
        fracy = fracx
        
    x= data['x']
    y = data['y']
    u = data['u']
    v = data['v']
    idx = []
    for i in range(0,x.shape[0],fracy):
        idx.append(i)
    x1 = x[idx]
    y1 = y[idx]
    u1 = u[idx]
    v1 = v[idx]
    
    idx = []
    for i in range(0,x1.shape[1],fracx):
        idx.append(i)
    x1 = x1[:,idx]
    y1 = y1[:,idx]
    u1 = u1[:,idx]
    v1 = v1[:,idx]
    
    data = {'x': x1, 'y':y1,
            'u': u1, 'v':v1}
    
    if normalize:
        data['z'] = (data['u']**2+data['v']**2)**0.5
        data['u'] = data['u']/data['z']
        data['v'] = data['v']/data['z']
    
    ax.quiver(data['x'],data['y'],data['u'],data['v'],scale=scale,width=width,headwidth=headwidth,**kwargs)
    return ax
    
def plot_colorbar(ax=None,cax=None,vmax='max',vmin='min',colormap=None,
                  ctitle=None,font_size=None,cticks=11,roundto=1,clabel=None,rotation=270,labelpad=10,
                  titlepad=10, ticklabels:list=None):
    if vmax == 'max':
        vmax = 1
    if vmin == 'min':
        vmin = 0
    
    cmap = _plt.get_cmap(colormap,256)
    norm = _mpl.colors.Normalize(vmin=vmin,vmax=vmax)
    sm = _plt.cm.ScalarMappable(cmap=cmap,norm=norm)
    
    ticks1 =  _np.linspace(vmin,vmax,cticks,endpoint=True).round(roundto)
    
    if cax is None:
        if ax is None:
            ax = _plt.gca()
        cbar = _plt.colorbar(sm,ax=ax,ticks=ticks1,orientation='vertical')
    else:
        cbar = _plt.colorbar(sm,cax=cax,ticks=ticks1,orientation='vertical')
    
    # cbar.set_ticklabels(ticks1)
    cbar.set_ticks(ticks1)
    if ctitle is not None:
        cbar.ax.set_title(ctitle,fontsize=font_size,pad=titlepad)
    if clabel is not None:
        cbar.set_label(clabel,rotation=rotation,labelpad=labelpad)
    if font_size is not None:
        cbar.ax.tick_params(labelsize=font_size)
    if ticklabels is not None:
        cbar.ax.set_yticklabels(ticklabels)
    return ax


def plot_contourf(vel_set=None,n=0,data=None,z='u',ax=None,vmax='max',vmin='min',
                  add_colorbar=True,colormap=None,ctitle=None,font_size=None,cticks=10,levels=200,alpha=1,
                  roundto=1,clabel=None,rotation=270,labelpad=10,qtile=0.01,equalize_at='min'):
    '''plot contourf for the velocity_set
    plots filled contour of a scalar either from vel_set or data, whichever is defined. If vel_set is defined then n (image number), 'z'(saclar to plot) is to be
    defined. If both vel_set and data are defined then data is given the priority above vel_set.

    Parameters
    ----------
    vel_set : velocity_set, optional
        either provide the velocity set or the data for plotting. The default is None.
    n : int, optional
        image/frame number. This is used when vel_set is supplied to the function. If data is directly given then this option is not useful. The default is 0.
    data : dict, optional
        dictionary-like object containing 'x','y',and 'z' keys and numpy_masked array like values. The 'z' values are contour filled in 'x' and 'y' coordinates.
        This is optional if the vel_set is defined. The default is None.
    z : str, optional
        scalar to plot, it can be from 'u,v,velocity_magnitude, omega_z, Wz, TKE'. The default is 'u'. This is used only when vel_set is defined.
    ax : matplotlib.pyplot.axes like, optional
        axes on which to plot. The default is None. If not specified then plt.gca() is used for plotting.
    vmax : float, optional
        maximum value in colorbar. The default is 'max'.
    vmin : float, optional
        minimum values in colorbar. The default is 'min'.
    add_colorbar : TYPE, optional
        DESCRIPTION. The default is True.
    colormap : TYPE, optional
        DESCRIPTION. The default is 'jet'.
    ctitle : TYPE, optional
        DESCRIPTION. The default is ''.
    font_size : TYPE, optional
        DESCRIPTION. The default is None.
    cticks : TYPE, optional
        DESCRIPTION. The default is 10.
    levels : TYPE, optional
        DESCRIPTION. The default is 200.
    alpha : TYPE, optional
        DESCRIPTION. The default is 1.
    roundto : TYPE, optional
        DESCRIPTION. The default is 2.
    qtile : float, optional
        DESCRIPTION. The default is 0.01. This is the quantile value to calculate vmax and vmin from z data.
    equalize_at : str, optional
        DESCRIPTION. The default is 'min'. The colorbar is equalized such that zero remains at the center. if 'min' then min(abs(vamx),abs(vmin)) is taken and if
        'max' then max is taken.

    Returns
    -------
    ax : matplotlib.pyplot.axes like
        returns the axes with plot

    '''
    
    if ax is None:
        ax = _plt.gca()
    if data is None:
        data = vel_set.make_contour_data(n=n,z=z)
    if (vmax == 'max') and (vmin=='min'):
        if qtile == 0:
            vmax = data['z'].data.max()
            vmin = data['z'].data.min()
        else:
            vmax = _np.quantile(data['z'].data,1-qtile).round(roundto)
            vmin = _np.quantile(data['z'].data,qtile).round(roundto)
        
        if (vmin==0) or (vmax==0):
            pass
        elif ((vmax /abs(vmax)) == (vmin/abs(vmin))):
            pass
        else:
            if equalize_at == 'min':
                v1 = min(abs(vmax),abs(vmin))
            if equalize_at == 'max':
                v1 = max(abs(vmax),abs(vmin))
            vmax = v1 * vmax / abs(vmax)
            vmin = v1 * vmin / abs(vmin)
    if vmax == 'max':
        vmax = _np.quantile(data['z'].data,0.99).round(roundto)
    if vmin == 'min':
        vmin = _np.quantile(data['z'].data,0.01).round(roundto)
    
    cmap = _plt.get_cmap(colormap,256)
    norm = _mpl.colors.Normalize(vmin=vmin,vmax=vmax)
    
    cp = ax.contourf(data['x'],data['y'],data['z'],
                     levels=levels,cmap=cmap,norm=norm,corner_mask=True,alpha=alpha)
    
    if add_colorbar:
        plot_colorbar(ax=ax,vmax=vmax,vmin=vmin,colormap=colormap,ctitle=ctitle,
                     font_size=font_size,cticks=cticks,roundto=roundto,clabel=clabel,rotation=rotation,labelpad=labelpad)
    
    return ax


def plot_image(vel_set=None,n=0,frame=0,data=None,ax=None,vmin=0,vmax=3000,levels=20,colormap='viridis',alpha=1):
    
    if ax is None:
        ax = _plt.gca()
    
    if data is None:
        data = vel_set.make_image_data(n=n,frame=frame)
    
    cmap = _plt.get_cmap(colormap,256)
    norm = _mpl.colors.Normalize(vmin=vmin,vmax=vmax)
    
    cp = ax.contourf(data['x'],data['y'],data['z'],levels=levels,corner_mask=True,
                     cmap=cmap,norm=norm,alpha=alpha)
    return ax


def plot_streamlines(vel_set=None,n=0,data=None,ax=None,density=(5,5),linewidth=1,color='white',**kwargs):
    
    if ax is None:
        ax = _plt.gca()
    
    if data is None:
        data = vel_set.make_streamline_data(n=n)
    
    ax.streamplot(data['x'],data['y'],data['u'][::-1],data['v'][::-1],
                  density=density,linewidth=linewidth,color=color,**kwargs)
    
    return ax



