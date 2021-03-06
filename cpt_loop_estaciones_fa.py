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
              ubiacion_cpt = '/home/edwin/Downloads/CPT/15.7.6',
              dir_salida = '/media/edwin/6F71AD994355D30E/Edwin/alexander/loop/amj_folder',
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
              spi_lenght = 3,
              datos_reales = False,
              iso_lineas = True,
              missing_val_x = -999,
              missing_val_y = -999):




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
    #Primer punto
    #os.getcwd(dir_salida)
    actual_dir = dir_salida+'/'
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

        # Estos condicionales son puestos porque si los
        # límites sobrepasan los límites (0 ó 360), entonces se tienen que ajustar
        if (el) > 360:
            el = (el)-360 
        
        if wl < 0:
            wl = 360 - wl
        
        base_x2 = pd.DataFrame({'lon':[dx2],
                                 'lon_iz':[wl],
                                 'lon_de':[el]})
        base_x = base_x.append(base_x2)
        
        dx2 += paso
        
        
    
    # Se crea la base que va a almacenar los resultados de la interpolación
    columns_1 = base_x.lon.tolist()    
    matriz_final = pd.DataFrame(index=base_y.lat.tolist(), columns = columns_1)
    matriz_lat_sup = pd.DataFrame(index=base_y.lat.tolist(), columns = columns_1)
    matriz_lat_inf = pd.DataFrame(index=base_y.lat.tolist(), columns = columns_1)
    matriz_lon_iz = pd.DataFrame(index=base_y.lat.tolist(), columns = columns_1)
    matriz_lon_de = pd.DataFrame(index=base_y.lat.tolist(), columns = columns_1)
    os.chdir(ubiacion_cpt)#Ojo se tiene que ejecutar donde se pueda ejecutar el ./CPT.exe
    os.popen('touch salida.txt') # Se crea este archivo para que luego se elimine
    for coun_lat, (lat, lat_sup, lat_inf) in enumerate(zip(base_y.lat, base_y.lat_sup, base_y.lat_inf)):
        print('====================================',str(coun_lat+1)+' de '+str(len(base_y.lat)), '============================================================================')
        for coun_lon, (lon, lon_iz, lon_de) in enumerate(zip(base_x.lon, base_x.lon_iz, base_x.lon_de)):
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
                if datos_reales == True: # Es verdadero cuando se usa con datos reales y es falso cuando se usa con daots modelados
                    print(month_forecast, file=f) # First month of season to forecast
                    print(lenght_of_season, file=f)# Length of season to forecast
                    print(spi_lenght, file=f) # Length of SPI
                print(nor_lat, file=f)
                print(sur_lat, file=f)
                print(wes_lon, file=f)
                print(eas_lon, file=f)
                print(minimum_number_modes_y, file=f)
                print(maximum_number_modes_y, file=f)
                print(minimum_number_modes_cca, file=f)
                print(maximum_number_modes_cca, file=f)

                ## Para seleccionar los valores missing values
                print('544', file=f)
                print(missing_val_x, file=f)
                print('10', file=f)
                print('10', file=f)
                print('1', file=f)
                print('1', file=f)
                print(missing_val_y, file=f)
                print('10', file=f)
                print('10', file=f)
                print('1', file=f)
                print('1', file=f)
                ## Fin de los valores missing

## # las nuevas líneas
##                 print('4', file=f)
##                 print('1982', file=f)
##                 print('5', file=f)
##                 print('1982', file=f)
##                 print('6', file=f)
##                 print('2019', file=f)
##                 print('9', file=f)
##                 print('1', file=f)
##                 print('531', file=f)
##                 print('3', file=f)
##                 print('7', file=f)
##                 print('36', file=f)
##                 print('8', file=f)
##                 print('3', file=f)
##                 print('541', file=f)
##                 print('542', file=f)
##                 print('544', file=f)
##                 print('-999', file=f)
##                 print('10', file=f)
##                 print('10', file=f)
##                 print('1', file=f)
##                 print('4', file=f)
##                 print('-999', file=f)
##                 print('10', file=f)
##                 print('10', file=f)
##                 print('1', file=f)
##                 print('4', file=f)
##                 print('554', file=f)
##                 print('2', file=f)
##                 print('133', file=f)
## #Fin de las nuevas lineas             

                print('311', file=f)
                print('131', file=f) # Dar formato a la salida
                print('2', file=f) # Formato definido
                print('0', file=f)
            
            os.popen('rm salida.txt')   # Usado para darle tiempo al procesamiento
            #time.sleep(1)
            valor_1 = os.popen('./CPT.x < script_loop.txt > salida.txt')
            valor_1.read() # es un paso que parece innecesaro pero se debe hacer para que se respete el tiempo del procesamiento del código en bash
            valor_1.close()
            #while 'salida.txt' not in os.listdir(): # usado para dare tiempo al procesamiento, es por prevensión, pero creo que no es necesario
            #    time.sleep(2)
                
                
            
            valor = os.popen("""awk '{print $8 "\t"}' salida.txt | grep -e "^0" -e "^-0" | tail -1""")   
            vt_1 = valor.read()
            valor.close()
            vt_2 = pd.to_numeric(vt_1[:-3])
            print('valor ', vt_2) # Imprime el valor tomado
            
                        
            matriz_final.iloc[coun_lat, coun_lon]  = vt_2
            
    
            matriz_lat_sup.iloc[coun_lat, coun_lon] = lat_sup 
            matriz_lat_inf.iloc[coun_lat, coun_lon] = lat_inf 
            matriz_lon_iz.iloc[coun_lat, coun_lon] = lon_iz 
            matriz_lon_de.iloc[coun_lat, coun_lon] = lon_de 
    
    ff = open(actual_dir+str(raster)+'.asci', 'w')
    with open(actual_dir+str(raster)+'.asci', 'w') as ff:
        print('ncols '+str(len(matriz_final.columns.values)), file=ff)
        print('nrows '+str(len(matriz_final.index)), file=ff)
        print('xllcenter '+str(base_x.lon.tolist()[0] - 360), file=ff) # Toca restarle 360 para que la imagen quede mejor
        print('yllcenter '+str(base_y.lat.tolist()[-1]), file=ff)
        print('cellsize '+str(paso), file=ff)
        print('nodata_value -9999', file=ff)
        print(matriz_final.to_string(index=False, header=False), file=ff)
    
############ ASCII de los valores de x e y

    ff = open(actual_dir+str(raster)+'_lon_de.asci', 'w')
    with open(actual_dir+str(raster)+'_lon_de.asci', 'w') as ff:
        print('ncols '+str(len(matriz_lon_de.columns.values)), file=ff)
        print('nrows '+str(len(matriz_lon_de.index)), file=ff)
        print('xllcenter '+str(base_x.lon.tolist()[0] - 360), file=ff) # Toca restarle 360 para que la imagen quede mejor
        print('yllcenter '+str(base_y.lat.tolist()[-1]), file=ff)
        print('cellsize '+str(paso), file=ff)
        print('nodata_value -9999', file=ff)
        print(matriz_lon_de.to_string(index=False, header=False), file=ff)

    ff = open(actual_dir+str(raster)+'_lon_iz.asci', 'w')
    with open(actual_dir+str(raster)+'_lon_iz.asci', 'w') as ff:
        print('ncols '+str(len(matriz_lon_iz.columns.values)), file=ff)
        print('nrows '+str(len(matriz_lon_iz.index)), file=ff)
        print('xllcenter '+str(base_x.lon.tolist()[0] - 360), file=ff) # Toca restarle 360 para que la imagen quede mejor
        print('yllcenter '+str(base_y.lat.tolist()[-1]), file=ff)
        print('cellsize '+str(paso), file=ff)
        print('nodata_value -9999', file=ff)
        print(matriz_lon_iz.to_string(index=False, header=False), file=ff)

    ff = open(actual_dir+str(raster)+'_lat_inf.asci', 'w')
    with open(actual_dir+str(raster)+'_lat_inf.asci', 'w') as ff:
        print('ncols '+str(len(matriz_lat_inf.columns.values)), file=ff)
        print('nrows '+str(len(matriz_lat_inf.index)), file=ff)
        print('xllcenter '+str(base_x.lon.tolist()[0] - 360), file=ff) # Toca restarle 360 para que la imagen quede mejor
        print('yllcenter '+str(base_y.lat.tolist()[-1]), file=ff)
        print('cellsize '+str(paso), file=ff)
        print('nodata_value -9999', file=ff)
        print(matriz_lat_inf.to_string(index=False, header=False), file=ff)

    ff = open(actual_dir+str(raster)+'_lat_sup.asci', 'w')
    with open(actual_dir+str(raster)+'_lat_sup.asci', 'w') as ff:
        print('ncols '+str(len(matriz_lat_sup.columns.values)), file=ff)
        print('nrows '+str(len(matriz_lat_sup.index)), file=ff)
        print('xllcenter '+str(base_x.lon.tolist()[0] - 360), file=ff) # Toca restarle 360 para que la imagen quede mejor
        print('yllcenter '+str(base_y.lat.tolist()[-1]), file=ff)
        print('cellsize '+str(paso), file=ff)
        print('nodata_value -9999', file=ff)
        print(matriz_lat_sup.to_string(index=False, header=False), file=ff)


##### FInal de la escritura de los archivos ascii



    # Escritura de los archivos finales, estos son las salidas en csv de los archivos finales
    matriz_final.to_csv(actual_dir + raster + '.csv')
    base_x.to_csv(actual_dir + raster + '_base_x.csv')
    base_y.to_csv(actual_dir + raster + '_base_y.csv')

    ###Creación del archivo NetCDF
    #os.popen('rm '+actual_dir+raster+'.nc') # Se crean estos archivos temporales, porque si el archivo está repetido presenta un error.
    os.popen('touch '+actual_dir+raster+'.nc') # Se crean estos archivos temporales, porque si el archivo está repetido presenta un error.
    dataset = Dataset(actual_dir+raster+'.nc', 'w', fromat='NETCDF4_CLASSIC') 
    level = dataset.createDimension('level', 0) 
    lat = dataset.createDimension('lat', len(base_y.lat))
    lon = dataset.createDimension('lon', len(base_x.lon)) 
    time = dataset.createDimension('time', None)

    times = dataset.createVariable('time', np   .float64, ('time',)) 
    levels = dataset.createVariable('level', np.int32, ('level',)) 
    latitudes = dataset.createVariable('latitude', np.float32,   ('lat',))
    longitudes = dataset.createVariable('longitude', np.float32,  ('lon',)) 

    corr = dataset.createVariable('cor_1', np.float32, ('time','level','lat','lon'))
            
    ### Adición de las longitudes y las latitudes al archivo netCDF
    lat_sup1 = dataset.createVariable('lat_sup1', np.float32, ('time','level','lat','lon'))
    lat_inf1 = dataset.createVariable('lat_inf1', np.float32, ('time','level','lat','lon'))
    lon_iz1 = dataset.createVariable('lon_iz1', np.float32, ('time','level','lat','lon'))
    lon_de1 = dataset.createVariable('lon_de1', np.float32, ('time','level','lat','lon'))
    
    if base_x.lon.tolist()[0] < 0:
        base_x.lon = base_x.lon + 360.0

    latitudes[:] = base_y.lat.tolist()
    longitudes[:] =  base_x.lon.tolist()
    
    #Llenado de los datos
    corr[0,0,:,:] = matriz_final.as_matrix()

    ### Llenado de las dimensiones en el archivo NetCDF
    lat_sup1[0,0,:,:] = matriz_lat_sup.as_matrix()
    lat_inf1[0,0,:,:] = matriz_lat_inf.as_matrix()
    lon_iz1[0,0,:,:] = matriz_lon_iz.as_matrix()
    lon_de1[0,0,:,:] = matriz_lon_de.as_matrix()

    ##Finalización del netcdf
    dataset.close()
    grafica_nc(archivo_nc = actual_dir+raster+'.nc', ancho = lon_2, alto = lat_2, paso = paso)
    



    return(matriz_final, base_x, base_y)# la Matriz final es la matriz que se tiene los datos de la extracción, 
                                        # Las bases de x e y son las bases que tienen las coordenadas
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

