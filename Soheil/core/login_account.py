from Soheil.config import DRIVER, START_LOGIN_BUTTON, PASSWORD_INPUT, EMAIL_INPUT
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


async def login_account(data):
    # wait untillogin button is available
    login_button = WebDriverWait(DRIVER, 30).until(
        EC.element_to_be_clickable((By.XPATH, START_LOGIN_BUTTON))
    )
    # click on login button
    data = json.loads(data)
    login_button.click()

    # Trying to input data in fields
    email_A = DRIVER.find_element(By.XPATH, EMAIL_INPUT)
    pass_A = DRIVER.find_element(By.XPATH, PASSWORD_INPUT)
    email_A.send_keys(data.get("email"))
    pass_A.send_keys(data.get("password"))

    # click on login
    DRIVER.find_element(By.XPATH, '//*[@id="logInBtn"]').click()
