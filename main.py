import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import os

# Opciones de voz / idioma
id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
id2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_texto():
    # Almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:
        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzo la grabacion
        print("Ya puedes hablar")

        # Guardar el audio
        audio = r.listen(origen)

        try:
            # Buscar en google
            pedido = r.recognize_google(audio, language="es-ES")

            # Imprimir prueba de ingreso
            print(f"Dijiste: {pedido}")

            # Devolver pedido
            return pedido
        except sr.UnknownValueError:
            # Prueba de que no comprendió audio
            print("Ups, no entendí")
            return "Sigo esperando"
        except sr.RequestError:
            # Prueba de que no comprendió audio
            print("Ups, no hay servicio")
            return "Sigo esperando"
        except:
            # Prueba de que no comprendió audio
            print("Ups, algo ha salido mal")
            return "Sigo esperando"

# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Informar el día de la semana
def pedir_dia():
    # Crear variable con datos de hoy
    dia = datetime.datetime.today()
    print(dia)

    # Crear variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario de los días
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # Decir el día de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")

# Informar qué hora es
def pedir_hora():
    # Crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    # Decir la hora
    hablar(hora)

# Función saludo inicial
def saludo_inicial():
    # Crear variable con datos de hora
    hora = datetime.datetime.now()

    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    # Decir saludo
    hablar(f"{momento} Juan, en qué te puedo ayudar?")

def ejecutarComando():
    hablar("¿Que comando de git quieres ejecutar?")
    pedido = transformar_audio_texto().lower()
    if "init" in pedido:
        os.system("git init")
        hablar("Se ejecuto el comando git init")
    if "agregar" in pedido:
        os.system("git add .")
        hablar("Se ejecuto el comando git add punto")

    if "commit" in pedido:
        hablar("Dale un nombre a tu commit")
        pedido = transformar_audio_texto().lower()
        os.system("git commit -am " + "\"" + pedido + "\"")
        hablar("se genero el commit con el nombre " + pedido)

    return

# Función central del asistente
def centro_pedido():
    # Saludo inicial
    saludo_inicial()
        
    # Variable de corte
    comenzar = True

    while comenzar:
        # Activar el micrófono y guardar el pedido en un String
        pedido = transformar_audio_texto().lower()

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
            pedido = pedido.replace("reproducir", "").strip()
            pywhatkit.playonyt(pedido)
            continue

        elif "comando" in pedido:
            ejecutarComando()

        elif "git" in pedido:
            ejecutarComando()
        
        elif "adiós" in pedido:
            hablar(f"Nos vemos, avisame si necesitas otra cosa Juan")
            break


centro_pedido()



