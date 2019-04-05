#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:55:13 2019
script para encontrar áreas en el cpt
Para datos de las estaciones
@author: edwin
"""
import pandas as pd
import numpy as np
import pdb
import os
import time
from netCDF4 import Dataset
from mapas_matplot_lib import grafica_nc

#nlat_1 = 28; slat_1 = -6; wlon_1 = 162; elon_1 = 322; lat_2 = 12; lon_2 = 12
#pasox=0.55; pasoy = 0.55

#nlat_1 = 90, slat_1 = -90, wlon_1 = -10, elon_1 = 349,
def loop_area(nlat_1 = 28, slat_1 = -6, wlon_1 = 162, elon_1 = 322,# Coordenadas límites de los datos de X
              lat_2 = 10, lon_2 = 10, paso = 10, # Largo y ancho del dominio pequeño que se usará como información predictora y paso
              variable_x = '/home/edwin/.wine/drive_c/CPT/basura/sst_2000_2018.tsv',
              variable_y = '/home/edwin/.wine/drive_c/CPT/basura/precip_2000_2018.tsv', 
              minimum_number_modes_x = 1,
              maximum_number_modes_x = 5,
              nor_lat = 11, # Coordenadas que se van a predecir# Para los datos en grilla de los Y
              sur_lat = -4,
              wes_lon = 281,# Coordenadas que se van a predecir
              eas_lon = 291,# Coordenadas que se van a predecir
              minimum_number_modes_y = 1,
              maximum_number_modes_y = 5,
              minimum_number_modes_cca = 1,# Número de modos de la correlación canónica
              maximum_number_modes_cca = 3,
              raster = 'salida',# nombre del archivo de salida
              month_forecast = 3, # Mes que se va a pronosticar
              lenght_of_season = 3,# Longitud del periodo que se va a tener en cuenta para pronosticar
              spi_lenght = 3):




    # Función creada para buscar las áreas que mejores resultados presentan para 
    # correlacionar las SST con las estaciones.
    
    ## En el directorio que se va a usar debe estár el archivo CPT.x y este 
    ## se debe permitir realizar la compilación con el comando ./CPT.x 
    
    ##Con estos 3 ejemplos se observa el desplazamiento de las grillas a la derecha 
    ##y para abajo, porque cuando se tiene fijo las longitudes del subdomínio y se
    ##cambia sólo el paso, entonces se crean pixeles más finos que opcuparán la 
    ##posición ((longitud del subdomínio)/2). Esto quiere decir que el primer pixel
    ##tendrá centro en la misma ubicación
    #matriz_15 = loop_area(paso=15, raster='paso15', lat_2 = 10, lon_2 = 10)
    #matriz_10_15 = loop_area(paso=10, raster='paso10_15', lat_2 = 10, lon_2 = 10)
    #matriz_5_15 = loop_area(paso=5, raster='paso5_15', lat_2 = 10, lon_2 = 10)
    #         
    #Cuando se valla a hacer mapas es mejor usar la proyección EPSG=3832

    ###Condicional para evitar el paso de las longituded

    print(elon_1)
    #pdb.set_trace()
    #Primer punto
    actual_dir = os.getcwd()+'/'
    dx1 = wlon_1 + (lon_2 /2)
    dy1 = nlat_1 - (lat_2 / 2)
    
    #Copia de seguridad del punto 1 se inicia en la esquina superior
    dx2 = dx1
    dy2 = dy1
    
    #Base para los valoers de la latitud
    base_y = pd.DataFrame()
    
    while dy2 > slat_1:
        nl = dy2 + (lat_2 / 2)
        sl = dy2 - (lat_2 / 2)
        
        base_y2 = pd.DataFrame({'lat':[dy2],
                                'lat_sup':[nl],
                                'lat_inf':[sl]})
        base_y = base_y.append(base_y2)
        
        dy2 -= paso
        #print(nl, sl)
    
    #Base para los valoers de la longitud
    base_x = pd.DataFrame()        
    
    while dx2 < elon_1:
        wl = dx2 - (lon_2 / 2)
        el = dx2 + (lon_2 / 2)

        if (el) > 360:
            el = (el)-360 
        
        base_x2 = pd.DataFrame({'lon':[dx2],
                                 'lon_iz':[wl],
                                 'lon_de':[el]})
        base_x = base_x.append(base_x2)
        
        dx2 += paso
        
        
    
    # Se crea la base que va a almacenar los resultados de la interpolación
    columns_1 = base_x.lon.tolist()    
    matriz_final = pd.DataFrame(index=base_y.lat.tolist(), columns = columns_1)
    #pdb.set_trace()    
    os.chdir('/home/edwin/Downloads/CPT/15.7.6')#Ojo se tiene que ejecutar donde se pueda ejecutar el ./CPT.exe
    os.popen('touch salida.txt') # Se crea este archivo para que luego se elimine
    for coun_lat, (lat, lat_sup, lat_inf) in enumerate(zip(base_y.lat, base_y.lat_sup, base_y.lat_inf)):
        print('====================================',str(coun_lat)+' de '+str(len(base_y.lat)), '============================================================================')
        for coun_lon, (lon, lon_iz, lon_de) in enumerate(zip(base_x.lon, base_x.lon_iz, base_x.lon_de)):
            #pdb.set_trace()
            print(lat, lon)
            
            #f = open('script-'+str(lat)+'-'+str(lon)+'.txt', 'w')
            #with open('script-'+str(lat)+'-'+str(lon)+'.txt', 'w') as f:
            
            f = open('script_loop.txt', 'w')
            with open('script_loop.txt', 'w') as f:

                print('611', file=f)
                print('1', file=f)
                print(variable_x, file=f)
                print(lat_sup, file=f)
                print(lat_inf, file=f)
                print(lon_iz, file=f)
                print(lon_de, file=f)
                print(minimum_number_modes_x, file=f)
                print(maximum_number_modes_x, file=f)
                print('2', file=f)
                print(variable_y, file=f)
                #print(month_forecast, file=f) # First month of season to forecast
                #print(lenght_of_season, file=f)# Length of season to forecast
                #print(spi_lenght, file=f) # Length of SPI
                print(nor_lat, file=f)
                print(sur_lat, file=f)
                print(wes_lon, file=f)
                print(eas_lon, file=f)
                print(minimum_number_modes_y, file=f)
                print(maximum_number_modes_y, file=f)
                print(minimum_number_modes_cca, file=f)
                print(maximum_number_modes_cca, file=f)
                #print('533', file=f)
                #print('4', file=f)
                #print('2', file=f)
                #print('-1.3', file=f)
                #print('-1.6', file=f)
                print('311', file=f)
                print('131', file=f) # Dar formato a la salida
                print('2', file=f) # Formato definido
                print('0', file=f)
            
            os.popen('rm salida.txt')   # Usado para darle tiempo al procesamiento
            #time.sleep(1)
            #pdb.set_trace()
            valor_1 = os.popen('./CPT.x < script_loop.txt > salida.txt')
            valor_1.read() # es un paso que parece innecesaro pero se debe hacer para que se respete el tiempo del procesamiento del código en bash
            valor_1.close()
            #while 'salida.txt' not in os.listdir(): # usado para dare tiempo al procesamiento, es por prevensión, pero creo que no es necesario
            #    time.sleep(2)
                
                
            
            valor = os.popen("""awk '{print $8 "\t"}' salida.txt | grep -e "^0" -e "^-0" | tail -1""")   
            vt_1 = valor.read()
            valor.close()
            vt_2 = pd.to_numeric(vt_1[:-3])
            
                        
            matriz_final.iloc[coun_lat, coun_lon]  = vt_2
    
    ff = open(actual_dir+str(raster)+'.asci', 'w')
    with open(actual_dir+str(raster)+'.asci', 'w') as ff:
        print('ncols '+str(len(matriz_final.columns.values)), file=ff)
        print('nrows '+str(len(matriz_final.index)), file=ff)
        print('xllcenter '+str(base_x.lon.tolist()[0] - 360), file=ff) # Toca restarle 360 para que la imagen quede mejor
        print('yllcenter '+str(base_y.lat.tolist()[-1]), file=ff)
        print('cellsize '+str(paso), file=ff)
        print('nodata_value -9999', file=ff)
        print(matriz_final.to_string(index=False, header=False), file=ff)
    
    


    ###Creación del archivo NetCDF
    os.popen('touch '+actual_dir+raster+'.nc') # Se crean estos archivos temporales, porque si el archivo está repetido presenta un error.
    os.popen('rm '+actual_dir+raster+'.nc')
    dataset = Dataset(actual_dir+raster+'.nc', 'w', fromat='NETCDF4_CLASSIC') 
    #dataset = Dataset('hola.nc', 'w', fromat='NETCDF4_CLASSIC') 
    level = dataset.createDimension('level', 0) 
    lat = dataset.createDimension('lat', len(base_y.lat))
    lon = dataset.createDimension('lon', len(base_x.lon)) 
    time = dataset.createDimension('time', None)

    times = dataset.createVariable('time', np   .float64, ('time',)) 
    levels = dataset.createVariable('level', np.int32, ('level',)) 
    latitudes = dataset.createVariable('latitude', np.float32,   ('lat',))
    longitudes = dataset.createVariable('longitude', np.float32,  ('lon',)) 

    corr = dataset.createVariable('cor_1', np.float32, ('time','level','lat','lon'))

    latitudes[:] = base_y.lat.tolist()
    longitudes[:] =  base_x.lon.tolist()
    
    #Llenado de los datos
    #pdb.set_trace()              
    corr[0,0,:,:] = matriz_final.as_matrix()

    ##Finalización del netcdf
    dataset.close()
    #pdb.set_trace()
    grafica_nc(archivo_nc = actual_dir+raster+'.nc')



    return(matriz_final)       
#pdb.set_trace()
#matriz_15 = loop_area(paso=15, raster='paso15', lat_2 = 10, lon_2 = 10)
#lmatriz_15 = loop_area(nlat_1 = 32, slat_1 = -30, wlon_1 = 174, elon_1 = 288,# Coordenadas límites de los datos de X
#        lat_2 = 10, lon_2 = 10, paso = 10, # Largo y ancho del dominio pequeño que se usará como información predictora y paso
#        variable_x = '/home/edwin/Downloads/CPT/15.7.6/data/ERSST_OND_1982-2014.tsv',
#        variable_y = '/home/edwin/Downloads/CPT/15.7.6/data/CPT_Estac_llanos_chirps_Ok2.csv', 
#        minimum_number_modes_x = 1,
#        maximum_number_modes_x = 5,
#        nor_lat = 6, # Coordenadas que se van a predecir# Para los datos en grilla de los Y
#        sur_lat = 3,
#        wes_lon = -75,# Coordenadas que se van a predecir
#        eas_lon = -71,# Coordenadas que se van a predecir
#        minimum_number_modes_y = 1,
#        maximum_number_modes_y = 5,
#        minimum_number_modes_cca = 1,# Número de modos de la correlación canónica
#        maximum_number_modes_cca = 3,
#        raster = 'llano_p1',# nombre del archivo de salida
#        month_forecast = 3, # Mes que se va a pronosticar
#        lenght_of_season = 3,# Longitud del periodo que se va a tener en cuenta para pronosticar
#        spi_lenght = 3)

