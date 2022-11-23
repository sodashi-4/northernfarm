from selenium.webdriver.common.by import By

from custom_sleep import short_sleep, medium_sleep

import os
from dotenv import load_dotenv


load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


# XPATH
XPATH_SIGN_IN = os.getenv("XPATH_SIGN_IN")
XPATH_EMAIL = os.getenv("XPATH_EMAIL")
XPATH_PASSWORD = os.getenv("XPATH_PASSWORD")
XPATH_SIGN_IN_SUBMIT = os.getenv("XPATH_SIGN_IN_SUBMIT")

def login(driver, logger):
  driver.find_element(By.XPATH, XPATH_SIGN_IN).click()
  logger.info("click sign in")
  short_sleep()

  email_field = driver.find_element(By.XPATH, XPATH_EMAIL)
  email_field.send_keys(EMAIL)
  logger.info("input email")
  short_sleep()
  password_field = driver.find_element(By.XPATH, XPATH_PASSWORD)
  password_field.send_keys(PASSWORD)
  logger.info("input password")
  short_sleep()
  login_button = driver.find_element(By.XPATH, XPATH_SIGN_IN_SUBMIT)
  login_button.click()
  logger.info("click login button")
  medium_sleep()