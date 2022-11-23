from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from custom_sleep import short_sleep, medium_sleep

import os
import re
from time import sleep

from dotenv import load_dotenv



load_dotenv()

# XPATH
XPATH_MENU_HEADER = os.getenv("XPATH_MENU_HEADER")
XPATH_READER_MENU = os.getenv("XPATH_READER_MENU")
XPATH_PAGE_INPUT_MENU = os.getenv("XPATH_PAGE_INPUT_MENU")
XPATH_PAGE_INPUT_BOX = os.getenv("XPATH_PAGE_INPUT_BOX")
XPATH_TOTAL_PAGE = os.getenv("XPATH_TOTAL_PAGE")
XPATH_PAGE_NUMBER_SUBMIT = os.getenv("XPATH_PAGE_NUMBER_SUBMIT")
XPATH_DIRECTION = os.getenv("XPATH_DIRECTION")
XPATH_CURSOR_CONTENT = os.getenv("XPATH_CURSOR_CONTENT")
XPATH_NEXT_RIGHT_PAGE = os.getenv("XPATH_NEXT_RIGHT_PAGE")
XPATH_NEXT_LEFT_PAGE = os.getenv("XPATH_NEXT_LEFT_PAGE")

def parse_object(driver, title, logger,start_page=1 ):
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
  total_page = driver.find_element(By.XPATH, XPATH_TOTAL_PAGE).text
  logger.info(f"total page: {total_page}")
  position_input.send_keys(start_page)
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
  logger.info(f"the object direction is {direction}")

  logger.info("start parsing")
  os.makedirs(f"./data/{title}", exist_ok=True)
  total_page = int(re.sub(r"\D", "", total_page))
  for i in range(start_page, int(total_page)-1):
    if i % 10 == 0:
      logger.info(f"parsing page {i}")
    if i == 1:
      driver.save_screenshot(f'./data/{title}/cover.png')
    else:
      driver.save_screenshot(f'./data/{title}/p{i}.png')
    driver.find_element(By.XPATH, XPATH_CURSOR_CONTENT).click()
    sleep(1.5)
    if direction == 'right':
      next_page = driver.find_element(By.XPATH, XPATH_NEXT_RIGHT_PAGE)
    else:
      next_page = driver.find_element(By.XPATH, XPATH_NEXT_LEFT_PAGE)
    try:
      next_page.click()
      short_sleep()
    except Exception as e:
      # for the page which take long time to load
      medium_sleep()
      try:
        next_page.click()
        short_sleep()
      except Exception as e:
        logger.error(e)
        return
  driver.close()
  