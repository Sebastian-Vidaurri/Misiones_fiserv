import PyPDF2
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet

def crear_pdf(lineas, nombre_archivo):
    c = canvas.Canvas(nombre_archivo, pagesize=landscape(letter))
    x_offset = -75
    style = getSampleStyleSheet()["Normal"]
    style.fontName = 'Courier'
    style.fontSize = 8
    y = 550

    for linea in lineas:
        if '\f\n' in linea:
            c.showPage()
            y = 550
            continue

        c.setFont(style.fontName, style.fontSize)
        c.drawString(100 + x_offset, y, linea.rstrip())
        y -= 10

    c.save()

def es_caratula(line):
    return "REPORTES PARA:" in line

def fin_pag(line):
    return "END;" in line

def rango(con):
    return con in range(1, 11) or con in range(20, 26) or con in range(38, 42) or con > 69

def procesar_archivo_txt(nombre_archivo_txt):
    lista_pdf = []
    con = 0
    caratula = False

    with open(nombre_archivo_txt, "r") as file_IN:
        for linea in file_IN:
            primer_caracter = linea[0]
            resto_cadena = linea[1:]

            if caratula:
                if rango(con) and not fin_pag(linea):
                    lista_pdf.append(resto_cadena)

                elif 'END;' in linea:
                    caratula = False

                con += 1
                continue

            if con == 50:
                lista_pdf.append('\f\n')
                con = 0
                continue

            if not linea.strip():
                lista_pdf.append('\n')
                continue

            if fin_pag(linea):
                continue

            if primer_caracter == '1':
                if 'FIRST DATA' in resto_cadena:
                    con = 1
                    lista_pdf.extend(['\f\n', resto_cadena])

                else:
                    lista_pdf.append('\f\n')
                    con = 0

            elif primer_caracter == '+':
                continue

            elif primer_caracter == ' ' or primer_caracter == '0':
                caratula = es_caratula(resto_cadena)
                lista_pdf.append(resto_cadena)
                con += 1

    return lista_pdf

def seleccionar_archivo_txt():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    nombre_archivo_txt = filedialog.askopenfilename(title="Selecciona un archivo TXT")

    return nombre_archivo_txt

if __name__ == "__main__":
    nombre_archivo_txt = seleccionar_archivo_txt()

    if nombre_archivo_txt:
        print("Archivo seleccionado:", nombre_archivo_txt)
        lista_pdf = procesar_archivo_txt(nombre_archivo_txt)
        nombre_archivo_pdf = "pruebas_horizontal.pdf"
        crear_pdf(lista_pdf, nombre_archivo_pdf)
        print(f"PDF creado exitosamente: {nombre_archivo_pdf}")
    else:
        print("No se seleccionó ningún archivo.")

### VER ACA EL LECTOR DE ARCHIVOS

import os

def leer_config(ruta_archivo):
    '''
    Lee la configuracion del programa
    El txt debe contener todos los campos utilizados

    config['IN']: ruta de entrada
    config['out']: ruta de salida
    '''
    config = {}
    try:
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            #ruta IN
            config['IN'] = lineas[0].strip()
            config['OUT'] = lineas[1].strip()
            
    except FileNotFoundError:
        print(f"El archivo '{ruta_archivo}' no se encontró.")
        
    except IOError:
        print(f"No se pudo leer el archivo '{ruta_archivo}'.")
        
    return config

def lista_nombres_archivos (ruta_carpeta):
    '''
    devuelve una lista con los nombres de los archivos existentes en una carpeta especifica
    '''
    try:
        # Lista para almacenar nombres de archivos
        lista_de_nombres = []
        
        # Iterar sobre los archivos en la carpeta
        for archivo in os.listdir(ruta_carpeta):
            # Verificar si es un archivo .txt
            if archivo.endswith('.txt'):
                lista_de_nombres.append(archivo)
        
        # Devolver la lista de nombres de archivos
        return lista_de_nombres
    
    except FileNotFoundError:
        print(f"La carpeta '{ruta_carpeta}' no se encontró.")
        return []
    except IOError:
        print(f"No se pudo leer la carpeta '{ruta_carpeta}'.")
        return []

def file_sin_procesar(ruta_in, ruta_out):
    '''
    devuelve los elementos de lista_in menos lista_out,
    se utilizara para obtener la lista de los elementos que aún no estan procesados
    '''
    try:
        #obtenemos las lista de los archivos que estan en las rutas de entrada y salida

        #TO_DO: seria mejor que la lista de salida las lea de un archivo que contenga el historial de los archivos procesados
        print('buscando txt la ruta: ', ruta_in)
        lista_in = lista_nombres_archivos(ruta_in)
        lista_out = lista_nombres_archivos(ruta_out)
        
        # Convertir ambas listas a conjuntos para realizar la diferencia
        set_in = set(lista_in)
        set_out = set(lista_out)
        
        # Obtener los archivos que están en lista_in pero no en lista_out
        archivos_faltantes = set_in - set_out
        
        # Devolver la lista de archivos faltantes
        return list(archivos_faltantes)
    
    except TypeError as e:
        print("Error:", e)
        return []




config = leer_config('config.txt') #busca la configuracion donde se encuentra el script

sin_procesar = file_sin_procesar(config['IN'], config['OUT'])

if sin_procesar == []:
    print('Nada por procesar')
else:
    print(sin_procesar)

