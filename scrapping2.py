import re
from colorama import Fore
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar opciones del navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecución en segundo plano
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Instalar y configurar el controlador de Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL de la página
url = 'https://www.zonaprop.com.ar'

# Abrir la página
driver.get(url)

# Obtener el contenido de la página
page_content = driver.page_source
print("page_content 🤯", page_content)
# Usar BeautifulSoup para analizar el contenido
soup = BeautifulSoup(page_content, 'html.parser')
containers = soup.find_all('div', class_='article-container-property')

# Imprimir los contenedores encontrados
print("containers", containers)
for aContainer in containers:
    print(aContainer)
    infoDepto = aContainer.find(class_='title-type-sup-property').text
    print(infoDepto)

# Cerrar el navegador
driver.quit()