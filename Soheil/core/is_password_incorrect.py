from Soheil.config import DRIVER, PASSWORD_OR_EMAIL_IS_INCORRECT
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


async def is_password_incorrect() -> bool:
    """
    check if backup code is correct
    """
    try:
        WebDriverWait(DRIVER, 30).until(
            EC.element_to_be_clickable((By.XPATH, PASSWORD_OR_EMAIL_IS_INCORRECT))
        )
        return False

    except:
        return True
