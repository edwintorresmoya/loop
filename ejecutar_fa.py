from cpt_loop_estaciones_fa import loop_area
lmatriz_15 = loop_area(nlat_1 = 35, slat_1 = 0, wlon_1 = 330, elon_1 = 360,# Coordenadas límites de los datos de X
        lat_2 = 30, lon_2 = 30, paso = 10, # Largo y ancho del dominio pequeño que se usará como información predictora y paso
        variable_x = '/media/edwin/6F71AD994355D30E/Edwin/alexander/usb/Rutina/input/CFS2_SST_AMJ_4Ic_1982_2019.tsv',
        variable_y = '/media/edwin/6F71AD994355D30E/Edwin/alexander/usb/Rutina/input/Y/Chumedo_IDEAM.csv',
        dir_salida = '/media/edwin/6F71AD994355D30E/Edwin/alexander/loop/amj_folder',
        ubiacion_cpt = '/home/edwin/Downloads/CPT/15.7.6',# Acá está el archivo que se ejecuta ./CPT.x
        minimum_number_modes_x = 1,
        maximum_number_modes_x = 10,
        nor_lat = 15, # Coordenadas que se van a predecir# Para los datos en grilla de los Y (Coordenadas del predictando)
        sur_lat = -5,
        wes_lon = -80,# Coordenadas que se van a predecir
        eas_lon = -60,# Coordenadas que se van a predecir
        minimum_number_modes_y = 1,
        maximum_number_modes_y = 10,
        minimum_number_modes_cca = 1,# Número de modos de la correlación canónica
        maximum_number_modes_cca = 5,
        raster = 'amj_chumedo_test',# nombre del archivo de salida
        month_forecast = 6, # Mes que se va a pronosticar
        lenght_of_season = 3,# Longitud del periodo que se va a tener en cuenta para pronosticar
        spi_lenght = 3, datos_reales = False, iso_lineas = False)

