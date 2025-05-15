import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_native_species_from_ebird(hotspot_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(hotspot_url)

    # Give time for JavaScript to load
    time.sleep(5)

    try:
        section = driver.find_element(By.CSS_SELECTOR, 'section[aria-labelledby="nativeNaturalized"]')
        species_elements = section.find_elements(By.CSS_SELECTOR, '.Species-common')
        species_names = [elem.text.strip() for elem in species_elements if elem.text.strip()]
    except Exception as e:
        print("Failed to find native species section:", e)
        species_names = []

    driver.quit()
    print("Found native/naturalized bird species:")
    return sorted(set(species_names))