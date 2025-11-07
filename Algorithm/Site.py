import random
from multiprocessing.spawn import set_executable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import requests


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

#options = webdriver.ChromeOptions()
#options.add_argument("--headless")
#options.add_argument("--disable-blink-features")
#options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument('--disable-extensions')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')

user_agent = random.choice(user_agents)

#options.add_argument(f'user-agent={user_agent}')

#driver = webdriver.Chrome(executable_path="C:\\Work\\chromedriver.exe", options=options)
#driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

#stealth(driver,
#        languages=["en-US", "en"],
#        vendor="Google Inc.",
#        platform="Win32",
#        webgl_vendor="Intel Inc.",
#        renderer="Intel Iris OpenGL Engine",
#        fix_hairline=True,
#        )


# def get_html(url):
#    driver.get(url)
#    return '<html>' + driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML') + "</html>"



def get_html(url):
   sess = requests.Session()
   sess.headers.update({"Connection": "close"})
   sess.headers.update({"Sec-Fetch-Mode": "navigate"})
   sess.headers.update({"Sec-Fetch-Site": "none"})
   sess.headers.update({"Sec-Fetch-User": "?1"})
   sess.headers.update({"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"})
   sess.headers.update(
       {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*"})
   sess.headers.update({"User-Agent": f"{user_agent}"})

   result = sess.get(url)

   return result.text





