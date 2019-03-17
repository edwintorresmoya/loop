"""
Script usado para hacer plots de los archivos netCDF4
Se creó la función grafica_nc y esta crea los archivos de salida
"""
from netCDF4 import Dataset as NetCDFFile 
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pdb
from mpl_toolkits.basemap import Basemap

def grafica_nc(archivo_nc='paso15.nc'):
    nc = Dataset(archivo_nc, mode='r')
    
    lat = nc.variables['latitude'][:]
    lon = nc.variables['longitude'][:]-360.
    time = nc.variables['time'][:]
    cor_1 = nc.variables['cor_1'][:] # Valores del goodnes index
    nc.close()
    lat_inter = (lat[0] - lat[-1]) / 10.0
    lon_inter = (lon[-1] - lon[0]) / 10.0
    map = Basemap(projection='merc',llcrnrlon=(lon[0]-(1*lon_inter)),llcrnrlat=(lat[-1]-(1*lat_inter)),urcrnrlon=(lon[-1]+(1*lon_inter)),urcrnrlat=(lat[0]+(1*lat_inter)),resolution='i') # projection, lat/lon extents and resolution of polygons to draw los valores adicionales se ponen para poder hacer más grandes o más pqueños los valores
    # resolutions: c - crude, l - low, i - intermediate, h - high, f - full
    
    
    map.drawcoastlines()
    map.drawstates()
    map.drawcountries()
    map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
    map.drawcounties() # you can even add counties (and other shapefiles!)
    
    
    parallels = np.arange(lat[-1],lat[0],abs(lat_inter*5)) # make latitude lines ever 5 degrees from 30N-50N
    meridians = np.arange(lon[0], lon[-1], abs(lon_inter)) # make longitude lines every 5 degrees from 95W to 70W
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    
    lons,lats= np.meshgrid(lon,lat) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
    x,y = map(lons,lats)
    
    
    clevs = np.arange(960,1040,4)
    cs = map.contour(x,y,cor_1[0,0,:,:],clevs,colors='blue',linewidths=1.)
    
    
    
    plt.clabel(cs, fontsize=9, inline=1) # contour labels
    plt.title('Mean Sea Level Pressure')
    
    temp = map.contourf(x,y,cor_1[0,0,:,:])
    cb = map.colorbar(temp,"bottom", size="5%", pad="2%")
    plt.title('Áreas de los mejores resultados.')
    cb.set_label('Índice')
    #pdb.set_trace()
    plt.savefig(archivo_nc[:-3]+'.png', figsize=(20,10) ,dpi = 199)
    #plt.show()

grafica_nc()
