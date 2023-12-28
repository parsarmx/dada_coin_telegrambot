from selenium import webdriver
from os import getenv
from dotenv import load_dotenv

load_dotenv("Soheil/.env")

DRIVER = webdriver.Chrome()
