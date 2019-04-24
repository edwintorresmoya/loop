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

def grafica_nc(archivo_nc='paso15.nc', iso_lineas = False, ancho = 9999, alto = 9999, paso = 9999):
    nc = Dataset(archivo_nc, mode='r')
    
    lat = nc.variables['latitude'][:]
    lon = nc.variables['longitude'][:] - 360.0
    time = nc.variables['time'][:]
    cor_1 = nc.variables['cor_1'][:] # Valores del goodnes index
    nc.close()
    lat_inter = (lat[0] - lat[-1]) / 10.0
    lon_inter = (lon[-1] - lon[0]) / 10.0
    if (((lon[0]-(1*lon_inter)) > -360) & ((lat[-1]-(1*lat_inter)) > -90) & (lat[0]+(1*lat_inter) < 90)):
        map = Basemap(projection='merc',llcrnrlon=(lon[0]-(1*lon_inter)),llcrnrlat=(lat[-1]-(1*lat_inter)),urcrnrlon=(lon[-1]+(1*lon_inter)),urcrnrlat=(lat[0]+(1*lat_inter)),resolution='i') # projection, lat/lon extents and resolution of polygons to draw los valores adicionales se ponen para poder hacer más grandes o más pqueños los valores
    else:
        map = Basemap(projection='merc',llcrnrlon=(lon[0]),llcrnrlat=(lat[-1]),urcrnrlon=(lon[-1]),urcrnrlat=(lat[0]),resolution='i') # projection, lat/lon extents and resolution of polygons to draw los valores adicionales se ponen para poder hacer más grandes o más pqueños los valores
    #map = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-360,urcrnrlon= 0,lat_ts=20,resolution='c')
    #map = Basemap(projection='geos',lon_0=-73,resolution='l') # usada para hacer la proyección del mundo redondo
    # resolutions: c - crude, l - low, i - intermediate, h - high, f - full
    
    
    map.drawcoastlines()
    map.drawstates()
    map.drawcountries()
    try:
        map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
    except:
        next
    map.drawcounties() # you can even add counties (and other shapefiles!)
    
    
    parallels = np.arange(lat[-1],lat[0],abs(lat_inter*2)) # make latitude lines ever 5 degrees from 30N-50N
    meridians = np.arange(lon[0], lon[-1], abs(lon_inter)) # make longitude lines every 5 degrees from 95W to 70W
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    meridians = map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    ## Esto es para rotar los ejes
    for m in meridians:
        try:
            meridians[m][1][0].set_rotation(45)
        except:
            pass
    
    lons,lats= np.meshgrid(lon,lat) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
    x,y = map(lons,lats)
    
    
    
    
    
    if iso_lineas == True:
        clevs = np.arange(np.nanmin(cor_1),np.nanmax(cor_1), (np.nanmax(cor_1) - np.nanmin(cor_1))/10)
        cs = map.contour(x,y,cor_1[0,0,:,:],clevs,colors='blue',linewidths=1.)
        plt.clabel(cs, fontsize=9, inline=1) # contour labels

    temp = map.contourf(x,y,cor_1[0,0,:,:])
    cb = map.colorbar(temp, size="5%", pad="2%")
    plt.title('Índice: ancho '+str(ancho)+' alto '+str(alto)+' paso '+str(paso))
    plt.savefig(archivo_nc[:-3]+'.png', figsize=(20,10) ,dpi = 199)
    #plt.show()            

#grafica_nc(archivo_nc = 'llano_25_25_5.nc', ancho = 55,alto = 44,paso = 3, iso_lineas = False)
#grafica_nc(archivo_nc = 'llano_25_25_5_todo_mundo.nc')
#grafica_nc(archivo_nc = 'llano_25_25_5_todo_munda.nc')
#grafica_nc()
