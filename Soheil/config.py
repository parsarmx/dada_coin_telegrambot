from selenium import webdriver
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")

DRIVER = webdriver.Chrome()
