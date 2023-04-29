import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def google_translate_ru_kk(text):

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    # https://translate.google.com/?sl=ru&tl=kk
    driver.get("https://translate.google.com/?sl=ru&tl=kk")
    source = driver.find_element(By.XPATH, "//textarea")
    source.clear()
    source.send_keys(text)
    source.send_keys(Keys.RETURN)
    # wait for the translation to appear
    wait = WebDriverWait(driver, 10)
    # get the translation from span "ryNqvb"
    translated_text = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='lRu31']")))
    translated_text = translated_text.text
    print(translated_text)
    driver.quit()

    return translated_text
