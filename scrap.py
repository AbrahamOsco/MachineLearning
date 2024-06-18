from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


MAP_ICONS_ZONA_PROP = {'icon-stotal':'surface_total_in_m2', 'icon-scubierta': 'surface_covered_in_m2', 'icon-ambiente': 'rooms'}

FIELDS_CSV = [
    "created_on", "property_type", "place_name", "place_with_parent_names", 
    "geonames_id", "lat-lon", "lat", "lon", "price", "currency", 
    "price_aprox_local_currency", "price_aprox_usd", "surface_total_in_m2", 
    "surface_covered_in_m2", "price_usd_per_m2", "price_per_m2", "floor", 
    "rooms", "expenses", "description", "title"
]


def get_dic_data(soup) -> dict:
    dic_data = {}
    for field in FIELDS_CSV: 
        dic_data[field] = ""
    created_on = soup.find('p', text=lambda text: text and "Publicado hace" in text)
    if created_on: 
        created_on_text = created_on.get_text(strip=True)
        print("created_on_text", created_on_text)
        days_created = 0
        if created_on_text.find('año') > 0:
            days_created = int(created_on_text.split(' ')[-2])*365
            print("days:", days_created)
        elif created_on_text.find('días') > 0:
            days_created = int(created_on_text.split(' ')[-2])
            print("days:", days_created)
        dic_data["created_on"] = (datetime.now() - timedelta(days = days_created)).strftime('%Y-%m-%d')
    
    price_div = soup.find('div', class_='price-value')
    price_usd = price_div.find('span').find('span').get_text(strip=True)
    if(len(price_usd) > 0):
        dic_data["price"] = price_usd.split(' ')[1]
    
    price_expenses = ''
    span_expensas = soup.find('span',class_ ='price-expenses')
    if (span_expensas):
        price_expenses = span_expensas.get_text(strip= True).split(' ')[2]
    dic_data["expenses"] = price_expenses
    
    image_thumbnail = soup.find('div', id='1').get('src')
    dic_data["image_thumbnail"] = image_thumbnail

    section_location_div = soup.find('div', class_='section-location-property section-location-property-classified')
    places_list = section_location_div.find('h4').get_text(strip=True).split(',')
    print("places_list", places_list)
    neighborhood = places_list[-2].strip()
    city = places_list[-1].strip()
    location_complete = f"Argentina | {neighborhood} | {city}"
    
    dic_data["place_with_parent_names"] = location_complete
    dic_data["place_name"] = neighborhood

    title = soup.find('div', class_= "section-title").find('h1', class_="title-property").get_text(strip=True)
    dic_data["title"] = title

    description_div = soup.select_one('section.article-section-description #reactDescription div div div')
    description = description_div.get_text(separator='\n', strip=True)
    dic_data["description"] = description
    
    icon_features = soup.find_all('li', class_='icon-feature')
    for feature in icon_features:
        icon = feature.find('i')
        icon_class = icon.get('class')[0]
        value = feature.get_text(strip =True).split()[0]
        if (icon_class in MAP_ICONS_ZONA_PROP.keys()):
            dic_data[ MAP_ICONS_ZONA_PROP[icon_class] ] = value
    return dic_data

def scrape_web_server():
    url = "https://www.zonaprop.com.ar/propiedades/clasificado/veclapin-venta-4-amb-c-depend-baulera-cochera-belgrano-53618255.html"
    options = Options()
    options.headless = True 
    driver_path = '/home/abraham/Escritorio/MachineLearningM/geckodriver'

    try:
        with webdriver.Firefox(service=Service(driver_path), options=options) as driver:
            driver.get(url)
            html = driver.page_source
            
            #Soup 
            soup = BeautifulSoup(html, 'html.parser')
            final_dic = get_dic_data(soup)
            print("final_dic",  final_dic)
           

    except Exception as e:
        print(f"Error al obtener la página con Selenium: {e}")

def main():
    scrape_web_server()

main()

