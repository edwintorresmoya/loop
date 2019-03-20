#Crear el archivo vacío
# Tomado de http://www.ceda.ac.uk/static/media/uploads/ncas-reading-2015/11_create_netcdf_python.pdf
from netCDF4 import Dataset
dataset = Dataset('llano_p1.nc', 'w', format='NETCDF4_CLASSIC')
print(dataset.file_format)

# Crear las dimensiones
level = dataset.createDimension('level', 10) 
lat = dataset.createDimension('lat', 73)
lon = dataset.createDimension('lon', 144) 
time = dataset.createDimension('time', None)

### Creación de las variables
import numpy as np

# Create coordinate variables for 4-dimensions
times = dataset.createVariable('time', np   .float64, ('time',)) 
levels = dataset.createVariable('level', np.int32, ('level',)) 
latitudes = dataset.createVariable('latitude', np.float32,   ('lat',))
longitudes = dataset.createVariable('longitude', np.float32,  ('lon',)) 
# Create the actual 4-d variable
temp = dataset.createVariable('temp', np.float32, ('time','level','lat','lon'))
# Acceso a las variables
for varname in dataset.variables.keys():
    var = dataset.variables[varname]
    print(varname, var.dtype, var.dimensions, var.shape)
# Atributos globales
import time

#Global attribute

dataset.description = 'bogus example script'  
dataset.history = 'Created ' + time.ctime(time.time())  
dataset.source = 'netCDF4 python module tutorial' 

dataset.description = 'bogus example script'  
dataset.history = 'Created ' + time.ctime(time.time())  
dataset.source = 'netCDF4 python module tutorial'
latitudes.units = 'degree_north'  
longitudes.units = 'degree_east'  
levels.units = 'hPa' 
temp.units = 'K' 
times.units = 'hours since 0001-01-01 00:00:00'  
times.calendar = 'gregorian' 

lats = np.arange(-90, 91, 2.5)
lons = np.arange(-180, 180, 2.5)
latitudes[:] = lats
longitudes[:] = lons


#Growing data along unlimited

from numpy.random import uniform
nlats = len(dataset.dimensions['lat'])
nlons = len(dataset.dimensions['lon'])
temp[0:5, :, :, :] = uniform(size=(5,10, nlats, nlons))
dataset.close()
