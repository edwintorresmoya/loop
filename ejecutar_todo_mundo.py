from cpt_loop_estaciones import loop_area
lmatriz_15 = loop_area(nlat_1 = 90, slat_1 = -90, wlon_1 = 0, elon_1 = 359,# Coordenadas límites de los datos de X
        lat_2 = 25, lon_2 = 25, paso = 5, # Largo y ancho del dominio pequeño que se usará como información predictora y paso
        variable_x = '/home/edwin/Downloads/CPT/15.7.6/data/cfs_MAM_icMay_82_19.csv',
        variable_y = '/home/edwin/Downloads/CPT/15.7.6/data/CPT_Estac_llanos_chirps_Ok2.csv',
        minimum_number_modes_x = 1,
        maximum_number_modes_x = 5,
        nor_lat = 6, # Coordenadas que se van a predecir# Para los datos en grilla de los Y (Coordenadas del predictando)
        sur_lat = 3,
        wes_lon = -75,# Coordenadas que se van a predecir
        eas_lon = -71,# Coordenadas que se van a predecir
        minimum_number_modes_y = 1,
        maximum_number_modes_y = 5,
        minimum_number_modes_cca = 1,# Número de modos de la correlación canónica
        maximum_number_modes_cca = 5,
        raster = 'llano_25_25_5_todo_mundo',# nombre del archivo de salida
        month_forecast = 6, # Mes que se va a pronosticar
        lenght_of_season = 3,# Longitud del periodo que se va a tener en cuenta para pronosticar
        spi_lenght = 3, datos_reales = False)

