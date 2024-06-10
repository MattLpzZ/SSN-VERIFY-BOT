import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

class SSNBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def run(self):
        try:
            for _ in range(100):
                combination = ''.join(str(random.randint(0, 9)) for _ in range(4))
                self.process_combination(combination)

        except KeyboardInterrupt:
            pass
        finally:
            self.driver.quit()

    def process_combination(self, combination):
        self.navigate_to_website()
        self.enter_data_and_submit(combination)
        self.process_next_page()
        time.sleep(5)  # Añadir tiempo de espera si es necesario

    def navigate_to_website(self):
        self.driver.get('https://www.ssn-verify.com/')

    def enter_data_and_submit(self, combination):
        input_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'series')))
        group_field = self.driver.find_element(By.ID, 'group')
        area_field = self.driver.find_element(By.ID, 'area')

        input_field.clear()
        input_field.send_keys(combination)
        group_field.send_keys('39')
        area_field.send_keys('117')

        # Cambiar al iframe
        try:
            self.driver.switch_to.frame('aswift_6')
        except NoSuchElementException:
            print("Iframe 'aswift_6' not found. Proceeding without switching.")

        # Hacer clic en el botón "Verify Now" dentro del iframe
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="ssn-submit" and @class="form-control input-lg btn btn-primary"]')))
        submit_button.click()

        # Cambiar de nuevo al contenido principal
        self.driver.switch_to.default_content()

    def process_next_page(self):
        # Esperar a que la siguiente página cargue (puedes ajustar el tiempo de espera según sea necesario)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]'))
        )

        # Analizar y procesar la página actual
        page_content = self.driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')

        rows = soup.find_all('div', {'class': 'row'})

        for i, row in enumerate(rows, start=1):
            tds = row.find_all('td')
            row_text = '\t'.join(td.get_text(strip=True) for td in tds)

            # Guardar el texto extraído en un archivo
            output_filename = os.path.join(self.output_folder, f'data_{time.time()}_{i}.txt')
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(row_text)

        # Volver a la página anterior
        self.driver.execute_script("window.history.go(-1)")

if __name__ == "__main__":
    ssn_bot = SSNBot()
    ssn_bot.run()
