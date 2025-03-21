#Importamos "dearpygui" para crear la interfaz grafica
import dearpygui.dearpygui as dpg

#Importamos "time" para lograr actualizar la pagina cada 5 segundos
import time 
#Necesaria para poder aplicar la actualizacion, ya que permite una ejecucion independiente
import threading
# Importamos request para lograr acceder al servidor de binance y tener los precios
import requests



#Definimos la url y los  parametros de la solicitud mediante una funcion 
def peticion_precios ():
    url_btc = "https://api.binance.com/api/v3/ticker/price"
    params_btc = {"symbol": "BTCUSDT"}  # Par de trading: BTC/USDT
    # Realizamos la solicitud con "get"
    response_btc = requests.get(url_btc, params=params_btc)
    #Se verifica si se logra hacer conexion y se guarda la respuesta y se convierte en json
    if response_btc.status_code == 200:
        data_btc = response_btc.json()  
    #Mostramos un mensaje de error en caso de no acceder a lo solicitado   
    else:
        print(f"Error: {response_btc.status_code}")

    # Aqui se hace otra peticion pero en este caso para acceder a que direccion a tomado la moneda en las 24hrs
    url24_btc = "https://api.binance.com/api/v3/ticker/24hr"
    params24_btc = {"symbol": "BTCUSDT"} 

    response24_btc= requests.get(url24_btc, params=params24_btc)

    if response24_btc.status_code == 200:
        data24_btc = response24_btc.json()
        # En este caso comprobamos que  'priceChangePercent este presente en el diccionario 
        if 'priceChangePercent' in data24_btc:
            #Si es asi lo almacenamos en una variable para mostrarla posteriormente
            c24_btc = float(data24_btc['priceChangePercent'])
        else:
            print("Error: 'priceChangePercent' no encontrado en la respuesta.")

    else:
        print(f"Error: {response24_btc.status_code}")
        
        
    #Solicitamos con los mismos pasos solo que para la moneda 'ETHUSDT'
    url_eth = "https://api.binance.com/api/v3/ticker/price"
    params_eth = {"symbol": "ETHUSDT"}  # Par de trading: BTC/USDT

    response_eth = requests.get(url_eth, params=params_eth)

    if response_eth.status_code == 200:
        data_eth = response_eth.json()  
    else:
        print(f"Error: {response_eth.status_code}")

    # Solicitamos ahora las 24hrs para la moneda 'ETHUSDT'
    url24_eth = "https://api.binance.com/api/v3/ticker/24hr"
    params24_eth = {"symbol": "ETHUSDT"} 

    response24_eth = requests.get(url24_eth, params=params24_eth)
    if response24_eth.status_code == 200:
        data24_eth = response24_eth.json()
        if  'priceChangePercent' in data24_eth:
            c24_eth = float(data24_eth[ 'priceChangePercent']) 
        else:
         print("Error: 'priceChangePercent' no encontrado en la respuesta.")

    else:
        print(f"Error: {response24_btc.status_code}")
            

    #Solicitamos con los mismos pasos solo que para la moneda 'BNBUSDT'
    url_bnb = "https://api.binance.com/api/v3/ticker/price"
    params_bnb = {"symbol": "BNBUSDT"}  

    response_bnb = requests.get(url_bnb, params=params_bnb)

    if response_bnb.status_code == 200:
        data_bnb = response_bnb.json()  
    else:
        print(f"Error: {response_bnb.status_code}")
    # Solicitamos ahora las 24hrs para la moneda 'BNBUSDT'    
    url24_bnb = "https://api.binance.com/api/v3/ticker/24hr"
    params24_bnb = {"symbol": "BNBUSDT"}

    response24_bnb = requests.get(url24_bnb, params=params24_bnb)

    if response24_bnb.status_code == 200:
        data24_bnb = response24_bnb.json()
        if 'priceChangePercent' in data24_bnb:
            c24_bnb = float(data24_bnb['priceChangePercent'])
        else:
            print("Error: : 'priceChangePercent' no encontrado en la respuesta ")
    else: 
        print(f"Error: {response24_bnb.status_code}")
    return data_btc,c24_btc,data_eth, c24_eth, data_bnb, c24_bnb
#Creamos una funcion que actualice los valores, modificando en tiempo real en la interfaz
def actualizar_inter():
    data_btc,c24_btc,data_eth, c24_eth, data_bnb, c24_bnb = peticion_precios()
    
    dpg.set_value("precio_btc", f"$ {data_btc['price']}")
    dpg.set_value("cambio_btc", f"{c24_btc}%")
    dpg.set_value("precio_eth", f"$ {data_eth['price']}")
    dpg.set_value("cambio_eth", f"{c24_eth}%")
    dpg.set_value("precio_bnb", f"$ {data_bnb['price']}")
    dpg.set_value("cambio_bnb", f"{c24_bnb}%")

    # Cambiar colores según el cambio porcentual
    if c24_btc > 0:
        dpg.configure_item("cambio_btc", color=(0, 255, 0))  # Verde si es positivo
    else:
        dpg.configure_item("cambio_btc", color=(255, 0, 0))  # Rojo si es negativo

    if c24_eth > 0:
        dpg.configure_item("cambio_eth", color=(0, 255, 0))  # Verde si es positivo
    else:
        dpg.configure_item("cambio_eth", color=(255, 0, 0))  # Rojo si es negativo

    if c24_bnb > 0:
        dpg.configure_item("cambio_bnb", color=(0, 255, 0))  # Verde si es positivo
    else:
        dpg.configure_item("cambio_bnb", color=(255, 0, 0))  # Rojo si es negativo
#Aqui creamos una funcion que con ayuda de las demas funciones actualizamos, en ella predeterminamos que se de cada 5 segundos 
def actualizacion_periodica():
    while True:
        actualizar_inter()
        time.sleep(5)  
#Creamos una ventana que contenga nuestro monitor de cripto y personalizamos al gusto
dpg.create_context()
dpg.create_viewport(title="MONITOR DE CRIPTOMONEDAS", width=800, height=200)       

with dpg.window(label="MonCript", width=800, height=210):
    dpg.add_text("Criptomonedas Diponibles", color=(255, 255, 0, 255))

    with dpg.table(header_row=True):
        dpg.add_table_column(label="Nombre")
        dpg.add_table_column(label="Simbolo")
        dpg.add_table_column(label="Precio")
        dpg.add_table_column(label="Cambio 24hrs")
# Se utilizo "tag" ya que es un identificador unico
        with dpg.table_row():
            dpg.add_text("Bitcoin")
            dpg.add_text("BTC")
            dpg.add_text("$", tag="precio_btc")
            dpg.add_text("", tag="cambio_btc")
            
            

        with dpg.table_row():
            dpg.add_text("Ethereum")
            dpg.add_text("ETH")
            dpg.add_text("$", tag="precio_eth")
            dpg.add_text("",tag="cambio_eth")
            

        with dpg.table_row():
            dpg.add_text("Binance Coin")
            dpg.add_text("BNB")
            dpg.add_text("$", tag="precio_bnb")
            dpg.add_text("",tag="cambio_bnb")

    with dpg.group(horizontal=True):
        dpg.add_spacer(width=350) 

# Se crea un boton sin funcionalidad, solo para decoracion ya que la interfaz de actualiza por si sola     
        with dpg.theme() as theme_button:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 150, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 170, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (30, 130, 230, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))

        button = dpg.add_button(label="Actualizar", width=100, height=30) 
        dpg.bind_item_theme(button, theme_button)
#Aqui se crea un nuevo objeto de hilo, para que el programa cierre cuando se cierre las pestaña principal
#De lo contrario se bloquearia la interfaz de usuario y no respondiera la aplicacion      
threading.Thread(target=actualizacion_periodica, daemon=True).start()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context() 