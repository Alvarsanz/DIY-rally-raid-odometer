import machine
from machine import Pin
from time import sleep
import tm1637
import tm1637_6d
import distance_GPS
import biestable
calculadora_distance=distance_GPS.DISTANCE_GPS()
#Accede al al libreria del display de 6 dígitos
tm_6_UP = tm1637_6d.TM1637_6(clk=Pin(27), dio=Pin(26))
tm_6_DOWN = tm1637_6d.TM1637_6(clk=Pin(27), dio=Pin(22))
#Accede a la libreria de calculo de distancias
calculate_distance = distance_GPS.DISTANCE_GPS()
#Accede al al libreria del display de 4 dígitos
tm_4 = tm1637.TM1637(clk=Pin(27), dio=Pin(21))
# Configura el pin 0 como entrada
pin5 = machine.UART(1, baudrate=9600, tx=None, rx= machine.Pin(5), txbuf=64)
#Configuración de los botones y leds
btn_01 = Pin(11, Pin.IN, Pin.PULL_DOWN)    #Bajar 10m en trips
btn_02 = Pin(12, Pin.IN, Pin.PULL_DOWN)    #Subir 10m en trips
btn_03 = Pin(13, Pin.IN, Pin.PULL_DOWN)    #Resetear trip parcial
btn_04 = Pin(14, Pin.IN, Pin.PULL_DOWN)    #Cambiar modo pantallas
btn_05 = Pin(15, Pin.IN, Pin.PULL_DOWN)    #Boton multifunción no asignado
led_01 = Pin(16, Pin.OUT)        #Led verde
led_02 = Pin(17, Pin.OUT)        #Led rojo 
#Configuración de la salida UART
uart = machine.UART(0, baudrate=9600, tx=None, rx=None, txbuf=64) # Configura la comunicación serie a través del puerto USB
change_mode = biestable.BIESTABLE()
#Puesta a cero de variables internas.
mode_04 = False # Cuando su valor sea 0, marcará la velocidad. Al cambiar a valor 1, marcará el rumbo.
mode_03 = False
tm_4.number(0)
odometer_enable = 0  # Configuración para registrar las primeras coordenadas para el odómetro
odometer_var = 0
parcial_odometer_var = 0
num_sat = 0
led_01.value(1)
led_02.value(0)
sleep(0.5)
gps_data = pin5.readline()  # Lee los datos del módulo GPS desde el pin 5 por primera vez

#Animación de encendido
tm_6_UP.show_6("buenos")
tm_6_DOWN.show_6(" dias ")
for n in range(0,11):   
    led_01.toggle()
    led_02.toggle()
    sleep(0.3)
tm_6_UP.show_6("      ")
tm_6_DOWN.show_6("      ")
led_01.value(0)
led_02.value(0)
while True:
    gps_data = pin5.readline()  # Lee los datos del módulo GPS desde el pin 5
    
    if gps_data:  # Verifica si se ha leído una línea válida
#Algunas veces el mensaje no es completo y no se puede decodificar. Para evitar fallo se introduce la siguiente linea.
        try:
            gps_data = gps_data.decode('ascii')  # Decodifica los datos NMEA en formato ascii 
        except UnicodeError:
            break
        print("data" , gps_data) # A modo de test muestra en pantalla los datos que ha leido

#Lectura de los diferentes mensajes suministrados por el GPS       
        strposition = gps_data.find("$GPRMC")  # Es capaz de detectar si se encuentra RMC en cualquier parte del string
        strvelocity = gps_data.find("$GPVTG")  # Es capaz de detectar si se encuentra VTG en cualquier parte del string
        strsatelites= gps_data.find("$GPGSV")  # Es capaz de detectar si se encuentra GSV en cualquier parte del string
        
        if strsatelites != -1:       # Cuando encuentra $GPGSV aparece distinto a -1.
            validdata = gps_data[strsatelites:]    #Divide en dos el scrip y se queda con la segunda parte.    
            validdata_parts = validdata.split(',')
            if len(validdata_parts) <= 20 and len(validdata_parts) >= 5:
                num_sat = validdata_parts[3]
                print("Número de satélites :", num_sat)
                
        
        if strposition != -1:       # Cuando encuentra $GPRMC aparece distinto a -1.
            validdata = gps_data[strposition:]    #Divide en dos el scrip y se queda con la segunda parte.    
            validdata_parts = validdata.split(',')
            if len(validdata_parts) == 13:
                time_stamp = validdata_parts[1]
                latitude = validdata_parts[3]
                longitude = validdata_parts[5]   #VALOR ESTANDARD 5
                speed = validdata_parts[7]
                try:
                    test_1 = time_stamp + latitude + longitude + speed # Comprueba que son valores válidos
                except SyntaxError:
                    break
                print("Tiempo:", time_stamp)
                print("Latitud:", latitude)
                print("Longitud:", longitude)
                print("Velocidad (nudos):", speed)
                               
                #Función de odómetro
                
                if len(str(latitude)) > 4 and len(str(longitude)) > 4 and len(str(latitude)) < 11 and len(str(longitude)) < 12  :
                    lat_parts = latitude.split('.')
                    lat_ent_1 = int(lat_parts[0])
                    lat_dec_1 = int(lat_parts[1])
                    print("    lat_ent_1 en main" ,lat_ent_1)
                    print("    lat_dec_1 en main " ,lat_dec_1)
                    long_parts = longitude.split('.')
                    long_ent_1 = int(long_parts[0])
                    long_dec_1 = int(long_parts[1])
                    print("    long_ent_1 en main" ,long_ent_1)
                    print("    long_dec_1 en main " ,long_dec_1) 
                    if odometer_enable == 1 :
                         (abs_distance_ent,abs_distance_dec)=calculate_distance.distance(lat_ent_0 , lat_dec_0 ,long_ent_0 , long_dec_0 , lat_ent_1 , lat_dec_1 , long_ent_1 , long_dec_1)
                         print("abs_distance_ent_main",abs_distance_ent)
                         print("abs_distance_dec_main",abs_distance_dec)
                         abs_distance = int(abs_distance_ent + abs_distance_dec)/10
                         print( "La distancia reccorrida es" , abs_distance)
                         
                         if abs_distance > 2.5 :       #Ajusta el filtro por debajo del cual no tiene en cuenta el movimiento (valor estandard 2.5)
                             odometer_var = odometer_var + abs_distance
                             parcial_odometer_var = parcial_odometer_var + abs_distance
                         print("distancia odometro",odometer_var)
                         lat_ent_0 = lat_ent_1
                         lat_dec_0 = lat_dec_1
                         long_ent_0 = long_ent_1
                         long_dec_0 = long_dec_1
                    else :                             #Toma valores iniciales con la primeras coordenadas
                        odometer_enable = 1
                        lat_ent_0 = lat_ent_1
                        lat_dec_0 = lat_dec_1
                        long_ent_0 = long_ent_1
                        long_dec_0 = long_dec_1
                        
                        
                
                #Zona de imprimir en doslpalys
                        
                if len(time_stamp) > 1 and len(latitude) > 1 and len(longitude) > 1 and len(speed) > 1 and odometer_enable == 1:  #aqui se comprueba que el gps se esta comunicando con los satelites
                    tm_6_UP.number_6(int(odometer_var))
                    tm_6_DOWN.number_6(int(parcial_odometer_var))
                    led_01.value(1)
                    led_02.value(0)
                    
                else:
                    #En caso de no mostrar información lo indica en los displays junto con una animación de carga
                    tm_6_UP.scroll_6('BUSCANDO SATELITES')   #BUSCANDO SATELITES
                    tm_6_DOWN.number_6(int(float(num_sat)))
                    print("buscanco satelites")
                    led_02.toggle()
                    
            else:
                print("Fallo1")  #La cadena de caracteres que recibe es muy larga. Esto se pone para evitar fallos
        
       
        if strvelocity != -1:       # Cuando encuentra $GPVTG aparece distinto a -1.
            validdata = gps_data[strvelocity:]    #Divide en dos el scrip y se queda con la segunda parte.    
            validdata_parts = validdata.split(',')
            if len(validdata_parts) == 10:
                ground_velocity_km = validdata_parts[7]
                track_made_good = validdata_parts[3]
                print("Velocidad (km):", ground_velocity_km)
                print("Rumbo grados: " , track_made_good)
                #Zona de imprimir en dislpalys
                            
                if (mode_04 != True ):    #Modo velocidad (SOLO ACTIVO TRAS DETECTAR VELOCIDAD)
                    if  (len(ground_velocity_km) > 1):  #aqui se comprueba que el gps se esta comunicando con los satelites
                        speed_km = round(float(ground_velocity_km))
                        if speed_km > 5:       #Esta condición se pone para que el error de precisión del gps no haga oscilar el gps en estado de reposo. 
                            tm_4.number(speed_km)
                        else:
                            tm_4.number(0)
                    if  (len(ground_velocity_km) <= 1):
                            #En caso de no mostrar información lo indica en los displays junto con una animación de carga
                            tm_4.number(0)
        
                if (mode_04 == True ):     #Modo compass
                    if (len(track_made_good) > 1)  :     #aqui se comprueba que el gps detecte rumbo
                        track = round(float(track_made_good))
                    
                        tm_4.number(track)
                    if (len(track_made_good) <= 1) :
                        tm_4.show("fail")
                    print("estado",btn_01.value())
                else:
                    print("Fallo2")  #La cadena de caracteres que recibe es muy larga. Esto se pone para evitar fallos
                    
    # Sección de botones
    print ("boton 1 dado",btn_01.value())
    print ("boton 2 dado",btn_02.value())
    print ("boton 3 dado",btn_03.value())
    print ("boton 4 dado",btn_04.value())
    if btn_04.value() == 1:  # Verifica si el botón de cambiar modo está siendo presionado
        mode_04=change_mode.cambiar_estado()
        if mode_04 ==  True :          # Cambia el estado del biestable a "tocado"
            tm_4.scroll("SPEED")
            sleep(0.05)
            print("aqui falla")
        else:       # Cambia el estado del biestable de vuelta a "no tocado"
            tm_4.scroll("COMPASS")
            sleep(0.05)
          
    while btn_01.value() == 1:
         odometer_var = odometer_var + 10
         parcial_odometer_var = parcial_odometer_var + 10
         tm_6_UP.number_6(int(odometer_var)) 
         tm_6_DOWN.number_6(int(parcial_odometer_var))
         sleep(0.25)
         
    while btn_02.value() == 1:        #boton 2 
        if parcial_odometer_var >= 10 and odometer_var >= 10 :
            odometer_var = odometer_var - 10
            parcial_odometer_var = parcial_odometer_var - 10
        if parcial_odometer_var <= 10 and odometer_var >= 10 :
            odometer_var = odometer_var - 10
            parcial_odometer_var = 0
        if parcial_odometer_var <= 10 and odometer_var <= 10 :
            odometer_var = 0
            parcial_odometer_var = 0
        tm_6_UP.number_6(int(odometer_var))   
        tm_6_DOWN.number_6(int(parcial_odometer_var))
        sleep(0.25)
    
    if btn_03.value() == 1:        #boton 3
        tm_6_DOWN.show_6("accept")
        sleep(1)
        if btn_03.value() == 1:
        parcial_odometer_var = 0
        tm_6_DOWN.number_6(int(parcial_odometer_var))
        sleep(1)
                 
                
    print("tik")
    sleep(0.25)  # Puedes ajustar el tiempo de espera según tus necesidades. PREDETERMINADO
