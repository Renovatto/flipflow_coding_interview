import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # Modo headless
    chrome_options.add_argument('--no-sandbox')  # Necessário em ambientes Docker
    chrome_options.add_argument('--disable-dev-shm-usage')  # Prevenir problemas com /dev/shm
    chrome_options.add_argument('--disable-gpu')  # Desabilitar GPU para ambientes headless
    chrome_options.add_argument('--remote-debugging-port=9222')  # Evitar problemas de porta

    # Configurar User-Agent para simular um navegador real
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Configurações adicionais para evitar bloqueios
    chrome_options.add_argument('--start-maximized')  # Iniciar em modo maximizado
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Evitar detecção do Selenium
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remover flag de automação
    chrome_options.add_experimental_option('useAutomationExtension', False)  # Desabilitar extensões automáticas

    chrome_options.add_argument('--user-data-dir=/home/chrome')
    chrome_options.add_argument('--data-path=/home/chrome')
    chrome_options.add_argument('--disk-cache-dir=/home/chrome')

    service = Service('/usr/bin/chromedriver')  # Caminho para o ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Script para remover detecção de Selenium
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })

    # driver = webdriver.Chrome()
    # driver.maximize_window()
    URL = "https://www.carrefour.es/supermercado/congelados/cat21449123/c"
    driver.get(URL)

    # Get the html page source of the current page
    page_source = driver.page_source

    # Print the page source
    # print(page_source)

    fileToWrite = open("response.html", "w")
    fileToWrite.write(page_source)
    fileToWrite.close()

    # Localizar elementos de produtos
    products = []

    # Scroll para carregar mais produtos
    for _ in range(5):  # Ajuste o número de scrolls conforme necessário
        driver.execute_script("window.scrollBy(0, 500);")
        # Aguardar o carregamento completo da lista de produtos
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.product-card-list__list li'))
        )
    # time.sleep(50)
    product_list = driver.find_element(By.CSS_SELECTOR, 'ul.product-card-list__list')
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

            products.append({
                'title': title,
                'price': price,
                'image': image,
                'link': link
            })
        except NoSuchElementException:
            continue
        # finally:
        #     # Feche o navegador
        #     driver.quit()

    # time.sleep(15)
    driver.quit()
    # Retornar os produtos como JSON
    x = json.dumps(products, indent=4)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <url>")
        # sys.exit(1)
    main(sys.argv[1])
