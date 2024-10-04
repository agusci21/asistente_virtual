import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import os
import pyautogui 

id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
id2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

def transformar_audio_texto():
    r = sr.Recognizer()

    with sr.Microphone() as origen:
        r.pause_threshold = 0.8

        print("Ya puedes hablar")

        audio = r.listen(origen)

        try:
            pedido = r.recognize_google(audio, language="es-ES")

            print(f"Dijiste: {pedido}")

            return pedido
        except sr.UnknownValueError:
            print("Ups, no entendí")
            return "Sigo esperando"
        except sr.RequestError:
            print("Ups, no hay servicio")
            return "Sigo esperando"
        except:
            print("Ups, algo ha salido mal")
            return "Sigo esperando"

def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)

    engine.say(mensaje)
    engine.runAndWait()

def pedir_dia():
    dia = datetime.datetime.today()
    print(dia)

    dia_semana = dia.weekday()
    print(dia_semana)

    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    hablar(f"Hoy es {calendario[dia_semana]}")

def pedir_hora():
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    hablar(hora)

def cambiarNombre():
    hablar("¿Cuál es tu nombre?")
    pedido = transformar_audio_texto().lower()
    
    hablar("¿Tu nombre es: " + pedido + "?")
    pedido2 = transformar_audio_texto().lower()

    if "sí" in pedido2 or "si" in pedido2:
        with open('nombre.txt', 'w') as archivo:
            archivo.write(pedido.capitalize())  
        hablar("Tu nombre ha sido guardado.")
    elif "salir":
        return
    else:
        hablar("Entendido, intentemos de nuevo.")
        cambiarNombre()

def saludo_inicial():
    hora = datetime.datetime.now()

    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    hablar(f"{momento} {obtenerNombre()}, en qué te puedo ayudar?")

def ejecutarComando():

    keep = True
    while keep:
        hablar("¿Que comando de git quieres ejecutar?")
        pedido = transformar_audio_texto().lower()
        if "init" in pedido:
            os.system("git init")
            hablar("Se ejecuto el comando git init")
        elif "agregar" in pedido:
            os.system("git add .")
            hablar("Se ejecuto el comando git add punto")

        elif "commit" in pedido:
            hablar("Dale un nombre a tu commit")
            pedido = transformar_audio_texto().lower()
            os.system("git commit -am " + "\"" + pedido + "\"")
            hablar("se genero el commit con el nombre " + pedido)
        elif "ninguno" in pedido:
            hablar("Abandonando el asistente de guit")
            keep = False
        else:
            hablar("No te entendí, Di ninguno para abandonar el asistente de guit")

    return

def obtenerNombre():
    try:
        with open('nombre.txt', 'r') as archivo:
            contenido = archivo.read()
            if contenido:
                return contenido
            else:
                return ""
    except FileNotFoundError:
        with open('nombre.txt', 'w') as archivo:
            archivo.write("")
            return ""

def centro_pedido():
    nombre = obtenerNombre()
    saludo_inicial()
     
    comenzar = True
    estaReproduciendo = False

    while comenzar:
        pedido = transformar_audio_texto().lower()
        nombre = obtenerNombre()
        print(f"Comando recibido: {pedido}")

        if "abrir youtube" in pedido:
            hablar("Estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abrir navegador" in pedido or "abrir el navegador" in pedido:
            hablar("Estoy abriendo el navegador")
            webbrowser.open("https://www.google.com.ar")
            continue
        elif "que día es hoy" in pedido or "qué día es hoy" in pedido or "qué día es" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido or "que hora es" in pedido or "qué hora" in pedido:
            pedir_hora()
            continue
        elif "busca en internet" in pedido:
            hablar("Buscando informacion")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Reproduciendo")
            estaReproduciendo = True
            pedido = pedido.replace("reproducir", "").strip()
            pywhatkit.playonyt(pedido)
            continue

        elif "comando" in pedido:
            ejecutarComando()

        elif "git" in pedido:
            ejecutarComando()
        
        elif "nombre" in pedido:
            cambiarNombre()
        
        elif "pausar" in pedido:
            if estaReproduciendo:
                estaReproduciendo = False
                pyautogui.press('space')
                hablar("Pausado")

        elif "pausa" in pedido:
            if estaReproduciendo:
                estaReproduciendo = False
                pyautogui.press('space')
                hablar("Pausado")

        elif "continuar" in pedido:
             if estaReproduciendo == False:
                hablar("Sigue escuchando tu cancion")
                pyautogui.press('space')
        
        elif "saltear" in pedido:
            hablar("Salteando la canción actual")
            pyautogui.hotkey('shift', 'n')
        
        elif "subir" in pedido:
            veces = 1
            if "mucho" in pedido:
                veces = 5
            for i in range(veces):
                pyautogui.press('volumeup')
        elif "bajar" in pedido:
            veces = 1
            if "mucho" in pedido:
                veces = 5
            for i in range(veces):
                pyautogui.press('volumedown')

        elif "adiós" in pedido:
            hablar(f"Nos vemos, avisame si necesitas otra cosa {nombre}")
            break


centro_pedido()



