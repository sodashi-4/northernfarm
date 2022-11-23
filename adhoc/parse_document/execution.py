from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from custom_sleep import short_sleep, long_sleep
from login import login
from parse_object import parse_object

import os
import re
import json
import pickle
from logging import getLogger, config
from dotenv import load_dotenv

with open("../../utils/python_log_format/log_config.json") as f:
    config.dictConfig(json.load(f))
logger = getLogger(__name__)

load_dotenv()

URL = os.getenv("URL")
UA = os.getenv("UA")

# XPATH
XPATH_CONTENT_TITLES = os.getenv("XPATH_CONTENT_TITLES")
XPATH_UNSUPPORTED_MODAL = os.getenv("XPATH_UNSUPPORTED_MODAL")
XPATH_UNSUPPORTED_MODAL_CLOSE_BUTTON = os.getenv("XPATH_UNSUPPORTED_MODAL_CLOSE_BUTTON")

def main():
  logger.info("start parsing documents")
  options = webdriver.ChromeOptions()
  options.add_argument(f'user-agent={UA}')
  # options.add_argument('--headless')
  driver = webdriver.Chrome("./chromedriver", options=options)
  logger.info("driver has been initialized")
  driver.get(URL)
  short_sleep()
  login(driver, logger)
  logger.info("login success")

  object_list = driver.find_elements(By.XPATH, XPATH_CONTENT_TITLES)

  # change if move file to another directory
  f = open("./skip_list.pickle", "rb")
  skip_list = pickle.load(f)

  execution_dict = {}
  for obj in object_list:
      title = re.sub(r"\(.+\)", "", obj.text)
      if title not in skip_list:
          execution_dict[title] = obj
  
  index_window = driver.window_handles[0]
  for title, obj in execution_dict.items():
    obj.click()
    short_sleep()
    # check validation
    try:
      driver.find_element(By.XPATH, XPATH_UNSUPPORTED_MODAL).click()
      short_sleep()
      driver.find_element(By.XPATH, XPATH_UNSUPPORTED_MODAL_CLOSE_BUTTON).click()
      logger.info(f"{title} is unsupported")
      skip_list.append(title)
      short_sleep()
      continue
    except:
      long_sleep()
      logger.info(f"start parsing {title}")
      parse_object(driver, title, logger)
      logger.info(f"finish parsing {title}")
      skip_list.append(title)
      driver.switch_to.window(index_window)

  driver.quit()
  f = open("skip_list.pickle", "wb")
  pickle.dump(skip_list, f)
  logger.info("all documents have been parsed")

if __name__ == "__main__":
  main()