#pip install beautifulsoup4
#pip install requests
#pip install openpyxl
# pip install selenium beautifulsoup4 webdriver-manager

import re
from colorama import Fore
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.zonaprop.com.ar')
soup = BeautifulSoup(page.text, 'html.parser')
print("page.text 🔴", page.text)
containers = soup.find_all('div', 'article-container-property')

print("containers", containers)
for aContainer in containers:
    print(aContainer)
    infoDepto = aContainer.find(class_= 'title-type-sup-property').text
    print(infoDepto)