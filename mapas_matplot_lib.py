"""
Script usado para hacer plots de los archivos netCDF4
"""
from netCDF4 import Dataset as NetCDFFile 
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

nc = Dataset('paso15.nc', mode='r')

lat = nc.variables['latitude'][:]
lon = nc.variables['longitude'][:]
time = nc.variables['time'][:]
cor_1 = nc.variables['cor_1'][:] # Valores del goodnes index


map = Basemap(projection='merc',llcrnrlon=(lon[0]*0.8),(llcrnrlat=lat[-1]*.8),(urcrnrlon=lon[-1]*1.2),(urcrnrlat=lat[0]*1.2),resolution='i') # projection, lat/lon extents and resolution of polygons to draw
# resolutions: c - crude, l - low, i - intermediate, h - high, f - full


map.drawcoastlines()
map.drawstates()
map.drawcountries()
map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
map.drawcounties() # you can even add counties (and other shapefiles!)


parallels = np.arange(30,50,5.) # make latitude lines ever 5 degrees from 30N-50N
meridians = np.arange(-95,-70,5.) # make longitude lines every 5 degrees from 95W to 70W
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

lons,lats= np.meshgrid(lon-180,lat) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
x,y = map(lons,lats)


clevs = np.arange(960,1040,4)
cs = map.contour(x,y,mslp[0,:,:]/100.,clevs,colors='blue',linewidths=1.)



plt.clabel(cs, fontsize=9, inline=1) # contour labels
plt.title('Mean Sea Level Pressure')

temp = map.contourf(x,y,cor_1[0,0,:,:])
cb = map.colorbar(temp,"bottom", size="5%", pad="2%")
plt.title('2m Temperature')
cb.set_label('Temperature (K)')
plt.show()

