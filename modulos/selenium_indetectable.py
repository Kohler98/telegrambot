import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver.patcher import Patcher
from pathlib import Path


 
def iniciar_webdriver(headless = False, pos= "maximizada"):
    """
    Inicia un navegador de chrome y devuelve el objeto webdriver instanciado,
    pos indica la posicion del navegador en lapantalla {"maximizada"|"izquierda"|"derecha"}
    """
    # instanciamos las opciones de chrome
    uc_driver_path = Patcher(executable_path="C:/Users/victor/Downloads/chromedriver_win32/chromedriver") 
    #options = uc.ChromeOptions()
    options = uc.ChromeOptions()
    # desactivamos el guardado de credenciales

    options.add_argument("--password-store=basic")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service":False,
            "profile.password_manager_enabled": False,
        }
    )
    # inciamos el driver
 
    driver = uc.Chrome(
        options=options,
        headless=headless,
        log_level=3,
        version_main=116

    )

    # posicionamos la ventana segun corresponda

    if not headless:

        driver.maximize_window()
        if pos != "maximizada":
            # obtenemos la resolucion de la ventana
            ancho,alto = driver.get_window_size().values()
            if pos == "izquierda":
                # posicionamos la ventana en la mitad izquierda de la pantalla
                driver.set_window_rect(x=0,y=0, width=ancho//2, height=alto)

            elif pos == "derecha":
                driver.set_window_rect(x=ancho//2,y=0,width=ancho//2,height=alto)

    return driver

