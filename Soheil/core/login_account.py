from Soheil.config import (
    DRIVER,
    START_LOGIN_BUTTON,
    PASSWORD_INPUT,
    EMAIL_INPUT,
    SEND_CODE,
    LOGIN_BUTTON,
    EA_LOGIN_PATH,
)
from Soheil.core.pass_two_factor import pass_twofactor
from Soheil.core.is_password_incorrect import is_password_incorrect
from Soheil.functions import update_telegram_message
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json


async def login_account(data):
    is_logged_in = False
    data = json.loads(data)

    # wait untillogin button is available
    login_button = WebDriverWait(DRIVER, 30).until(
        EC.element_to_be_clickable((By.XPATH, START_LOGIN_BUTTON))
    )

    # click on login button
    login_button.click()

    # Trying to input data in fields
    email = DRIVER.find_element(By.XPATH, EMAIL_INPUT)
    password = DRIVER.find_element(By.XPATH, PASSWORD_INPUT)
    email.send_keys(data.get("email"))
    password.send_keys(data.get("password"))

    # click on login
    DRIVER.find_element(By.XPATH, LOGIN_BUTTON).click()
    if not await is_password_incorrect():
        await update_telegram_message(
            chat_id=data.get("chat_id"),
            message_id=data.get("message_id"),
            new_text="رمز اشتباه بیده",
        )

        # back to first page
        DRIVER.get(EA_LOGIN_PATH)
        return is_logged_in

    try:
        send_code = WebDriverWait(DRIVER, 30).until(
            EC.element_to_be_clickable((By.XPATH, SEND_CODE))
        )

        done = await pass_twofactor(
            backup_code=data.get("backup_code"),
            button=send_code,
            message_id=data.get("message_id"),
            chat_id=data.get("chat_id"),
        )

        # this should return a status to admin pannel that crawler trying to logging in

        if done:
            print(f"logged in; in {email} was successful")
            is_logged_in = True
            await update_telegram_message(
                data.get("chat_id"),
                data.get("message_id"),
                "logged in successfuly",
            )

        else:
            print(f"error while trying to login {data.get('email')}")

        return is_logged_in
    except NoSuchElementException:
        print("logged in without two-step code")
