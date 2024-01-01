from Soheil.config import DRIVER, TWO_STEP_CODE_INVALID
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def is_backup_code_is_correct() -> bool:
    """
    check if backup code is correct
    """
    try:
        WebDriverWait(DRIVER, 30).until(
            EC.element_to_be_clickable((By.XPATH, TWO_STEP_CODE_INVALID))
        )
        return False

    except:
        return True
