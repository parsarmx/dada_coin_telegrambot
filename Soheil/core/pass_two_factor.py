from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Soheil.core.is_backup_code_correct import is_backup_code_is_correct
from Soheil.core.is_logged_in_by_console import is_logged_in_by_console
from Soheil.functions import update_telegram_message

from Soheil.config import (
    DRIVER,
    TWO_FACTOR_CODE_INPUT,
    TWO_FACTOR_SIGN_IN_BUTTON,
    EA_LOGIN_PATH,
)


async def pass_twofactor(
    backup_code: str, button: WebElement, message_id: str, chat_id: str
):
    """
    trying to pass two factor page using backup_code
    """
    done = False
    try:
        button.click()

        # Trying to enter a two-factor code
        element = DRIVER.find_element(By.XPATH, TWO_FACTOR_CODE_INPUT)
        element.send_keys(backup_code)

        signin = WebDriverWait(DRIVER, 30).until(
            EC.element_to_be_clickable((By.XPATH, TWO_FACTOR_SIGN_IN_BUTTON))
        )
        signin.click()

        if not is_backup_code_is_correct():
            await update_telegram_message(
                chat_id, message_id, "رمز دو مرحله ای اشتباهه"
            )

            # back to first page
            DRIVER.get(EA_LOGIN_PATH)

            return done
        if not is_logged_in_by_console():
            await update_telegram_message(chat_id, message_id, "کنسول لاگینه!")

            # back to first page
            DRIVER.get(EA_LOGIN_PATH)

        done = True

    except Exception as e:
        print(e)
        return done

    return done
