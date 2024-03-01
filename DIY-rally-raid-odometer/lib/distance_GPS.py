from mpy_decimal import *

class DISTANCE_GPS(object):  #"""Libreria para medir la distancia entre dos puntos sin tener en cuent al altitud"""        
    def distance(self, lat_ent_0 , lat_dec_0 ,long_ent_0 , long_dec_0 , lat_ent_1 , lat_dec_1 , long_ent_1 , long_dec_1): 
        
        print(lat_ent_0 , lat_dec_0 ,long_ent_0 , long_dec_0 , lat_ent_1 , lat_dec_1 , long_ent_1 , long_dec_1)
        # Declaración de constantes
        pi_dn= DecimalNumber(3141592653580,12)
        c= DecimalNumber(1745329252,11)
        R = 6378000
        incremento_lat = DecimalNumber(111319444444, 6)
        a_dn = DecimalNumber(6378137,0)
        b_dn = DecimalNumber(63567523142,4)
        latitude_0 = lat_ent_0 + lat_dec_0
        len_lat_0 = len(str(lat_dec_0))+2
        latitude_1 = lat_ent_1 + lat_dec_1
        len_lat_1 = len(str(lat_dec_1))+2
        longitude_0 = long_ent_0 + long_dec_0
        len_long_0 = len(str(long_dec_0))+2
        longitude_1 = long_ent_1 + long_dec_1
        len_long_1 = len(str(long_dec_1))+2
        lat_0_dn = DecimalNumber(latitude_0,len_lat_0)
        lat_1_dn = DecimalNumber(latitude_1,len_lat_1)
        long_0_dn = DecimalNumber(longitude_0,len_long_0)
        long_1_dn = DecimalNumber(longitude_1,len_long_1)
         #Cambio a Radianes        
        lat_0_dn_rad = lat_0_dn * c
        lat_1_dn_rad = lat_1_dn * c
        long_0_dn_rad = long_0_dn * c
        long_1_dn_rad = long_1_dn * c
        #Cambio de latitud y longitud
        delta_lat = lat_1_dn - lat_0_dn
        print("delta_lat",delta_lat)
        delta_long = long_1_dn - long_0_dn
        #Metros recorridos debido a la latitud bajo un modelo esférico
        metros_lat = incremento_lat*delta_lat 
        #Metros recorridos debido a la longitud bajo un modelo WGS 84
        R_wgs_84_0=((((a_dn**2)*lat_0_dn_rad.cos())**2) + (((b_dn**2)*lat_0_dn_rad.sin())**2))/(((a_dn*lat_0_dn_rad.cos())**2) + ((b_dn*lat_0_dn_rad.sin())**2))
        R_wgs_84 = R_wgs_84_0.square_root()
        #ASUMIENDO APROXIMACIÓN WGS 84
        r_84= R_wgs_84*lat_0_dn_rad.cos()
        incremento_long = 2*pi_dn*r_84/360
        metros_long = delta_long * incremento_long
        dist_0 = metros_lat**2 + metros_long**2
        dist_total = dist_0.square_root()
        #Mostrar en pantalla
        print("incremento_lat",incremento_lat)
        print("incremento_long",incremento_long)
        print( "dist_total", dist_total)
        print ("metros_lat",metros_lat)
        print ("metros_long",metros_long)
        #Devolver valor
        abs_distance = str(dist_total)
        if dist_total != 0 :
            abs_distance_parts = abs_distance.split('.')
            abs_distance_ent = abs_distance_parts[0]
            abs_distance_dec = abs_distance_parts[1]
        else :
            abs_distance_ent = ("0")
            abs_distance_dec = ("0")
        return(abs_distance_ent,abs_distance_dec[0])
