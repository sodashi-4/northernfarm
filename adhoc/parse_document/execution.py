from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import os
import re
from time import sleep
from random import uniform
from dotenv import load_dotenv
load_dotenv()


URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
UA = os.getenv("UA")
START_PAGE = 321

# XPATH
XPATH_SIGN_IN = os.getenv("XPATH_SIGN_IN")
XPATH_EMAIL = os.getenv("XPATH_EMAIL")
XPATH_PASSWORD = os.getenv("XPATH_PASSWORD")
XPATH_SIGN_IN_SUBMIT = os.getenv("XPATH_SIGN_IN_SUBMIT")
XPATH_UNSUPPORTED_MODAL = os.getenv("XPATH_UNSUPPORTED_MODAL")
XPATH_MENU_HEADER = os.getenv("XPATH_MENU_HEADER")
XPATH_READER_MENU = os.getenv("XPATH_READER_MENU")
XPATH_PAGE_INPUT_MENU = os.getenv("XPATH_PAGE_INPUT_BOX")
XPATH_PAGE_INPUT_BOX = os.getenv("XPATH_PAGE_INPUT_BOX")
XPATH_PAGE_NUMBER_SUBMIT = os.getenv("XPATH_PAGE_NUMBER_SUBMIT")
XPATH_DIRECTION = os.getenv("XPATH_DIRECTION")
XPATH_CURSOR_CONTENT = os.getenv("XPATH_CURSOR_CONTENT")
XPATH_NEXT_RIGHT_PAGE = os.getenv("XPATH_NEXT_RIGHT_PAGE")
XPATH_NEXT_LEFT_PAGE = os.getenv("XPATH_NEXT_LEFT_PAGE")
XPATH_CONTENT_TITLES = os.getenv("XPATH_CONTENT_TITLES")

def short_sleep():
    sleep(uniform(2, 3))

def medium_sleep():
    sleep(uniform(7, 10))

def long_sleep():
    sleep(uniform(15, 20))

def login(driver):
  driver.find_element(By.XPATH, XPATH_SIGN_IN).click()
  short_sleep()

  email_field = driver.find_element(By.XPATH, XPATH_EMAIL)
  email_field.send_keys(EMAIL)
  short_sleep()
  password_field = driver.find_element(By.XPATH, XPATH_PASSWORD)
  password_field.send_keys(PASSWORD)
  short_sleep()
  login_button = driver.find_element(By.XPATH, XPATH_SIGN_IN_SUBMIT)
  login_button.click()
  medium_sleep()

def parse_object(driver, title):
  print(f"start {title}")
   # check validation
  try:
    driver.find_element(By.XPATH, XPATH_UNSUPPORTED_MODAL)
    print("unsupported object")
    return
  except:
    print("supported object")

  w = 1200
  h = 1600
  driver.set_window_size(w, h)
  driver.switch_to.window(driver.window_handles[1])

  # go to first page
  cursor = ActionChains(driver)
  cursor.move_to_element(driver.find_element(By.XPATH, XPATH_MENU_HEADER))
  cursor.perform()
  short_sleep()
  driver.find_element(By.XPATH, XPATH_READER_MENU).click()
  short_sleep()
  driver.find_element(By.XPATH, XPATH_PAGE_INPUT_MENU).click()
  short_sleep()
  position_input = driver.find_element(By.XPATH, XPATH_PAGE_INPUT_BOX)
  position_input.send_keys("321")
  short_sleep()
  # move to first 
  driver.find_element(By.XPATH, XPATH_PAGE_NUMBER_SUBMIT).click()
  medium_sleep()

  # check direction
  try:
    driver.find_element(By.XPATH, XPATH_DIRECTION)
    direction ='right'
  except:
    direction ='left'
  print(direction)

  print("start parsing")
  os.makedirs(f"./data/{title}", exist_ok=True)
  for i in range(START_PAGE,1200):
    print(f"page {i}")
    if i == 1:
      driver.save_screenshot(f'./data/{title}/cover.png')
    else:
      driver.save_screenshot(f'./data/{title}/p{i}.png')
    driver.find_element(By.XPATH, XPATH_CURSOR_CONTENT).click()
    sleep(1.5)
    try:
      if direction == 'right':
        driver.find_element(By.XPATH, XPATH_NEXT_RIGHT_PAGE).click()
      else:
        driver.find_element(By.XPATH, XPATH_NEXT_LEFT_PAGE).click()
      short_sleep()
    except Exception as e:
      medium_sleep()
      try:
        if direction == 'right':
          driver.find_element(By.XPATH, XPATH_NEXT_RIGHT_PAGE).click()
        else:
          driver.find_element(By.XPATH, XPATH_NEXT_LEFT_PAGE).click()
        short_sleep()
      except Exception as e:
        print(e)
        print("end")
        break
  driver.close()
  


def main():
  options = webdriver.ChromeOptions()
  options.add_argument(f'user-agent={UA}')
  options.add_argument('--headless')
  driver = webdriver.Chrome("./chromedriver", options=options)
  driver.get(URL)
  short_sleep()

  login(driver)
  

  object_list = driver.find_elements(By.XPATH, XPATH_CONTENT_TITLES)
  skip_list = []
  execution_dict = {}
  for i, obj in enumerate(object_list):
      if obj.text not in skip_list:
          title = re.sub(r"\(.+\)", "", obj.text)
          execution_dict[title] = obj
          print(f"{i}: {title}")
  
  i = 0
  for title, obj in execution_dict.items():
    if i == 1:
      break
    obj.click()
    long_sleep()
    print(f"start {title}")
    parse_object(driver, title)
    i += 1

  driver.quit()

if __name__ == "__main__":
  main()