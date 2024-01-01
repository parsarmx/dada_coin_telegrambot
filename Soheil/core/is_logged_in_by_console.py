from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Soheil.config import DRIVER, SIDNED_IN_BY_CONSOL_BUTTON, SIGNED_IN_BY_CONSOLE_TEXT


def is_logged_in_by_console():
    try:
        WebDriverWait(DRIVER, 60).until(
            EC.element_to_be_clickable((By.XPATH, SIDNED_IN_BY_CONSOL_BUTTON))
        )
        WebDriverWait(DRIVER, 60).until(
            EC.element_to_be_clickable((By.XPATH, SIGNED_IN_BY_CONSOLE_TEXT))
        )
        return False

    except:
        return True
