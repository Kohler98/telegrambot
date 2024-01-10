# modulos python

import os
import sys
import time
import pickle
import tempfile

# modulos de terceros
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# modulos propios
from modulos.config import *
from modulos.colores import *
from modulos.cursor_arriba import *
from modulos.selenium_indetectable import iniciar_webdriver

from bs4 import BeautifulSoup
class ChatGpt:

    def __init__(self, user,password, headless=False) -> None:
        self.OPENAI_USER = user
        self.OPENAI_PASS = password
        self.COOKIES_FILE = f'{tempfile.gettempdir()}/openai.cookies'
        print(f'{azul}Iniciando webdriver{gris_claro}')
        self.driver = iniciar_webdriver(headless=headless,pos="izquierda")
 
        self.wait = WebDriverWait(self.driver, 30)
        login = self.login_openai()

        print()

        if not login:
            sys.exit()

    def login_openai(self):

        """Realiza login ne openai por cookies o desde 0"""
        # login por cookies

        if os.path.isfile(self.COOKIES_FILE):
            print(f'\33[K{azul}LOGIN POR COOKIES{gris_claro}')
            # cargamos robots.txt del dominio correspondiente
            cookies = pickle.load(open(self.COOKIES_FILE,'rb'))
            self.driver.get("https://chat.openai.com/robots.txt")
            #añadimos las cookies al navegador
            for cookie in cookies:
                cursor_arriba()
                print(f'\33[K{gris_claro}cargando cookie: {cookie["name"]}{gris_claro}')
                try:
                    self.driver.add_cookie(cookie)

                except:
                    pass

            cursor_arriba()
            print(f'\33[K{gris_oscuro} cargando chatGpt{gris_oscuro}')
            self.driver.get("https://chat.openai.com/")
            # comprobamos si el login es correcto
            login = self.comprobar_login()

            if login:
                print(f'\33[K{gris_claro}LOGIN POR COOKIES: {verde}OK{gris_claro}')
                return login
            # si el login ha fallado
            else:
                print(f'\33[K{gris_claro}LOGIN POR COOKIES: {rojo}FALLIDO{gris_claro}')

        #LOGIN DESDE CEROO
        print(f'\33[K{azul}Login desde cero{gris_claro}')
        print(f'\33[K{gris_claro}cargando chatGPT{gris_claro}')
        self.driver.get("https://chat.openai.com/")
        cursor_arriba()
        #CLICK EN LOGIN
        print(f"\33[K{gris_claro}clic en 'login' {gris_claro}")
        e = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Log in']")))
        e.click()
        #INTRODUCIMOS USUARIO
        cursor_arriba()
        print(f'\33[K{gris_claro}introduciendo usuario{gris_claro}')
        e = self.wait.until(EC.element_to_be_clickable((By.ID,"username")))
        e.send_keys(self.OPENAI_USER)
        #CLICK EN "Continue"
        cursor_arriba()
        print(f'\33[K{gris_claro}click en "continue" {gris_claro}')
        e = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[name='action']")))
        e.click()

        cursor_arriba()
        print(f'\33[K{gris_claro}introduciendo contraseña{gris_claro}')
        e = self.wait.until(EC.element_to_be_clickable((By.ID,"password")))
        e.send_keys(self.OPENAI_PASS)
        #click continue

        cursor_arriba()
        print(f'\33[K{gris_claro}click en "continue" {gris_claro}')
        e = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".c72d38f49 button[name='action']")))
        e.click()
        # comprobamos si el login es correcto
        login = self.comprobar_login()
        # si el login es correcto
        if login:
            #guardamos las cookies
            pickle.dump(self.driver.get_cookies(), open(self.COOKIES_FILE,"wb"))
            print(f'\33[K{azul}LOGIN DESDE CERO:{verde}OK{gris_claro}')

        else:
            print(f"\33[K{azul}LOGIN DESDE CERO: {rojo}FALLDO{gris_claro}")
        return login
    
    def comprobar_login(self,tiempo = 30):

        """
        Devuelve true si estamos logueados y false en caso contrario
        tiempo: cantidad de segundos mientras los cuales se comprobara si el login es correcto
        """
        login = False


        while  tiempo >0:
            try:
                e = self.driver.find_element(By.XPATH,"//div[text()='Next']")
                e.click()
            except:
                pass
            # clic en "done" button.btn.relative.btn-primary
            try:
                e = self.driver.find_element(By.CSS_SELECTOR,"button.btn.relative.btn-primary")
                e.click()
                login = True
                break
            except:
                pass
   
            # # login correcto (click en la caja de texto)
            # try:
            #     e = self.driver.find_element(By.CSS_SELECTOR,"textarea[tabindex='0']")
            #     e.click()
            #     login = True
            #     break
            # except:
            #     pass

            # login incorrecto opcion 1
            try:
                e = self.driver.find_element(By.ID,"username")
                break
            except:
                pass
            # login incorrecto opcion 2
            try:
                e = self.driver.find_element(By.XPATH,"//div[text()='Log in]")
                break
            except:
                pass
            # session expirada
            try:

                e = self.driver.find_element(By.CSS_SELECTOR,"h3.text-lg")

                if  "session has expired" in e.text:
                    cursor_arriba()
                    print(f"{amarillo}\\33[KLA SESSION HA EXPIRADO{gris_claro}")
                    print()
                    break
            except:
                pass
            #pausa
            cursor_arriba()
            print(f"{gris_claro}\33[Kcomprobando login... {tiempo}{gris_claro}")
            time.sleep(1)
            tiempo-= 1

        # eliminamos el ultimo print
        cursor_arriba()
        print("\33[K")
        cursor_arriba(2)
        return login
    
    def chatear(self,prompt, formato):
        """
        Introduce un prompt u devuelve el resultado generado por chatGPT
        formato: "String" = devuelve la respuesta en texto plano
                  "html" = devuelve la respuesta en formato html(telebot)
        """
        e = self.driver.find_element(By.CSS_SELECTOR,"textarea[tabindex = '0']")
        e.send_keys(prompt)

        e = self.driver.find_element(By.CSS_SELECTOR,"button.absolute.p-1")
        e.click()
        respuesta = ""
        # verificar cuanto tiempo tarda en enviar la respuesta
        inicio = time.time()

        while True:

            #extraemos el texto generado
            try:
                e = self.driver.find_elements(By.CSS_SELECTOR,"div.markdown")[-1]
                respuesta = e.text
            except:
                pass
      
            try:
                #elemento de los 3 puntitos animados mientras s egenera la respueta

                e = self.driver.find_element(By.CSS_SELECTOR,"div.text-2xl")
                # si el elemento existe es porque se ha empezado a generar la respuesta

            except:
                # si los 3 puntitos ya no estan, es que la respuesta ha terminado
                if respuesta: # si se ha generado alguna respuesta
                    # salimos del buclque
                    break
            # mostramos el tiempo transcurrido
            segundos = int(time.time()-inicio)

            if segundos:
                print(f'\33[K{azul}Generando respuesta... {gris_claro}{segundos} ({len(respuesta)}){gris_claro}')
                time.sleep(1)
                cursor_arriba()
        # informamos el tiempo que ha tardado en generar la respuesta
        print(f'\33[K{morado}Respuesta generado en {blanco}{segundos} {morado}segundos{gris_claro}')

        #extraemos el texto generado otra vez por si faltaba algo
        e = self.driver.find_elements(By.CSS_SELECTOR,"div.markdown")[-1]
        # si el formato es string
        if formato == "string":
            # devolvemos el texto plano
            respuesta = e.text
        # si el formato deseado es html
        elif formato == "html":

            #obtenemos el texto de la respuesta en formato hmtl
            respuesta = self.formato_html()
        return respuesta
    
    def formato_html(self):
        """
        Pasea el codigo HTML de la pagina con BeautifulSoup
        Devuelve un string con las etiquetas html que correspondan (formato html telegram)
        """
        def html_tg_code(texto):
            """
            Cambia "<" y ">" del texto por las entidades
            correspondientes compatibles con telegram
            """
            return texto.replace("<","&lt;").replace('>','&gt;')
        def cambiar_etiquetas(texto):
            """
            Devuelve el texto con formato html valido para telegram
            Sustituye o elimina las etiquetas por las que corresponden
            """
            # eliminamos la etiqueta p

            texto = texto.replace('<p>','').replace('</p>','')

            # convertimos la etiqueta "string" en "b" (NEGRITA)
            texto = texto.replace('<strong>','<b>').replace('</strong>','</b>')
            # convertimos la etiqueta "em" en "i" (CURSIVA)
            texto = texto.replace('<em>','<i>').replace('</em>','</i>')
            # convertimos la etiqueta "del" en "s" (Tachado)
            texto = texto.replace('<del>','<s>').replace('</del>','</s>')
            return texto

        # inicializamos el string de salida
        salida = ""
        #preparamos la sopa del codigo hmtl de la pagina
        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        # elemento que contiene la ultima respuesta generada
        respuesta = soup.find_all("div",{"class":"markdown"})[-1]    
        # recorremos los subelementos

        for x in respuesta.contents:
            tag = x.name
            if tag == "p":
                # guardamos en un string el codigo html del elemento
                texto = str(x)

                # formateamos el texto

                texto = cambiar_etiquetas(texto)
                # añadimos el texto al string de salida
                salida+=f'{texto}\n\n'

            
            # si la etiqueta es de codigo
            elif tag == "pre":
                # obtenemos el texto plano de la etiqueta "code"

                texto = x.find("code").text
                # añadimos el texto al string de salida
                salida+=f'<code>{html_tg_code(texto)}</code>\n'
            # si la etiqueta es una lista con indice
            elif tag == "ol":
                # comprobamos si se indica un indice concreto en el atributo start
                n = x.attrs.get("start")
                # si se indica
                if n:
                    # lo convertimos en entero
                    n = int(n)
                # si no se indica
                else:
                    # incializamos el indice
                    n = 1
                    # recorremos los elementos
                    for y in x.content:
                        # si tiene texto con etiqueta "p"
                        texto = y.find("p")
                        if not texto:
                            texto = y
                        salida+=f'{n}. {cambiar_etiquetas(str(texto))}\n'
                        # si tiene texto con etiqueta "pre"
                        texto = y.find("pre")
                        if texto:
                            texto = y.find("code").text
                            salida+=f"<code>{html_tg_code(texto)}</code>\n" 
                        # aumentamos en 1 el indice

                        n+=1
                    #añadimos un salto de linea mas al finalizar la lista
                    salida+='\n'
            # si la etiqueta es de una lista no ordenada
            elif tag == "ul":
                # convertimos en string el codigo html del elemento
                texto = str(x)
                #eliminamos la etiqueta "ol" (CAJA DE LA LISTA)
                texto = texto.replace("<ul>",'').replace("</ul>","")
                # obtenemos cada uno de los parrafos de la lista partiendo por la etiqueta
                lista = texto.split("</li>")

                # recorremos la lista

                for item in lista:
                    # si tiene contenido
                    if item:
                        #eliminamos la etiqueta de inicio
                        texto = item.replace("<li>","")
                        #formateamos el texto

                        texto = cambiar_etiquetas(texto)

                        # añadimos el texto al string de salida incluyendo un guion al inicio
                        salida+=f'- {texto}\n'
                #añadimos un salto de linea mas al finalizar la lista
                salida+='\n'
        return salida
    
    def cerrar(self):
        print(f"\33[K{azul}Saliendo...{gris_claro}")
        self.driver.quit()
if __name__ == "__main__":
    
    chatgpt = ChatGpt(correo,clave)

    # bucle principal

    while True:
        prompt = input(f'{azul}Prompt (S=Salir):{gris_claro}')
        if prompt.lower() == "s":
            chatgpt.cerrar()
            sys.exit()
        else:
            # enviamos el prompt
            respuesta = chatgpt.chatear(prompt)
            prompt(f'\33[K{amarillo}{respuesta}{gris_claro}')
            print()