from selenium import webdriver
from selenium.webdriver.common.by import By
import time
def test_front_end_interaction():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000")

    url_input = driver.find_element(By.ID, "url")
    submit_button = driver.find_element(By.ID, "submit")

    url_input.send_keys("https://www.google.com")
    submit_button.click()
    result_div = driver.find_element(By.ID, "result")
    time.sleep(2)
    assert "http://localhost:8000" in result_div.text

    driver.quit()