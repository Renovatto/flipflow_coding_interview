from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import re
import json

def main(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # Modo headless
    chrome_options.add_argument('--no-sandbox')  # Necessário em ambientes Docker
    chrome_options.add_argument('--disable-dev-shm-usage')  # Prevenir problemas com /dev/shm
    chrome_options.add_argument('--disable-gpu')  # Desabilitar GPU para ambientes headless
    chrome_options.add_argument('--remote-debugging-port=9222')  # Evitar problemas de porta

    # Configurar User-Agent para simular um navegador real
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Define o zoom para 70%
    chrome_options.add_argument("--force-device-scale-factor=0.7")

    # Start config browser
    nav = webdriver.Chrome(options=chrome_options)
    try:
        # Navigate to url
        nav.get(url)

        # Script para remover detecção de Selenium
        nav.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })

        time.sleep(3)

        #####################################
        # TESTE PARA RECUPERAR HTML DA PAGINA
        page_source = nav.page_source
        fileToWrite = open("response.html", "w")
        fileToWrite.write(page_source)
        fileToWrite.close()
        #####################################

        # Localizar elementos de produtos
        products = []

        nav.save_screenshot("screenshot.png")  # Salve um screenshot para depuração
        # Scroll para carregar mais produtos
        for _ in range(5):  # Ajuste o número de scrolls conforme necessário
            nav.execute_script("window.scrollBy(0, 500);")
            # Aguardar o carregamento completo da lista de produtos
            WebDriverWait(nav, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.product-card-list__list li'))
            )

        product_list = nav.find_element(By.CSS_SELECTOR, 'ul.product-card-list__list')
        items = product_list.find_elements(By.CSS_SELECTOR, 'li')

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '.product-card__title').text.strip()
                price = item.find_element(By.CSS_SELECTOR, '.product-card__price').text.strip()
                price = float(re.sub(r'[^\d,]', '', price).replace(',', '.'))

                if not title or not price:
                    continue

                image = item.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

                # print(title, price)

                products.append({
                    'title': title,
                    'price': price,
                    'image': image,
                    'link': link
                })
            except NoSuchElementException:
                continue

    finally:
        data = json.dumps(products)
        #####################################
        # TESTE PARA VERIFICAR JSON
        fileToWrite = open("data.txt", "w")
        fileToWrite.write(data)
        fileToWrite.close()
        #####################################
        nav.save_screenshot("screenshot2.png")  # Salve um screenshot para depuração
        return data
        # Feche o navegador
        nav.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <url>")
        sys.exit(1)
    print(main(sys.argv[1]))

