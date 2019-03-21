from cpt_loop_estaciones import loop_area
lmatriz_15 = loop_area(nlat_1 = 32, slat_1 = -30, wlon_1 = 174, elon_1 = 288,# Coordenadas límites de los datos de X
        lat_2 = 5, lon_2 = 10, paso = 5, # Largo y ancho del dominio pequeño que se usará como información predictora y paso
        variable_x = '/home/edwin/Downloads/CPT/15.7.6/data/ERSST_OND_1982-2014.tsv',
        variable_y = '/media/edwin/6F71AD994355D30E/Edwin/alexander/datos/CPT_Estac_chirps_Centro_Ibague_cuencas_Ok2.csv',
        minimum_number_modes_x = 1,
        maximum_number_modes_x = 5,
        nor_lat = 5, # Coordenadas que se van a predecir# Para los datos en grilla de los Y
        sur_lat = 4,
        wes_lon = -76,# Coordenadas que se van a predecir
        eas_lon = -74,# Coordenadas que se van a predecir
        minimum_number_modes_y = 1,
        maximum_number_modes_y = 5,
        minimum_number_modes_cca = 1,# Número de modos de la correlación canónica
        maximum_number_modes_cca = 3,
        raster = 'ibague',# nombre del archivo de salida
        month_forecast = 3, # Mes que se va a pronosticar
        lenght_of_season = 3,# Longitud del periodo que se va a tener en cuenta para pronosticar
        spi_lenght = 3)

