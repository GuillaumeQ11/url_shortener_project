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
    button = driver.find_element(By.ID, "copy")
    assert button.is_displayed()

    driver.quit()

def test_same_slug_twice():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000")

    url_input = driver.find_element(By.ID, "url")
    slug_input = driver.find_element(By.ID, "slug")
    submit_button = driver.find_element(By.ID, "submit")

    url_input.send_keys("https://www.google.com")
    slug_input.send_keys("test_same_slug_twice")
    submit_button.click()
    time.sleep(2)
    submit_button.click()
    result_div = driver.find_element(By.ID, "result")
    time.sleep(2)
    assert "Le slug fourni est déjà utilisé." in result_div.text
    button = driver.find_element(By.ID, "copy")
    assert not button.is_displayed()


    driver.quit()