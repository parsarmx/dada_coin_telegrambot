from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Soheil.config import DRIVER, MESSAGE_FROM_EA_XPATH

# async def find_cart(name: str, amount: str):
#     done = False
