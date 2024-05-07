import utils
from promptflow import tool
from promptflow.connections import CustomConnection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@tool
def request_flow_login(
    connection: CustomConnection, input_text: str, use_cache=True
) -> str:
    URL = "https://citflowdevapim.azure-api.net/login?"
    COOKIE_NAME = "FlowToken"

    # Check if cache should be used and if data is cached
    if use_cache:
        cached_auth_token = utils.retrieve_cached_data("auth_token")
        if cached_auth_token:
            print("Auth token retrieved from cache:", cached_auth_token)
            return cached_auth_token

    # Baixar o webdriver removatente do navegador que você deseja usar
    # https://sites.google.com/a/chromium.org/chromedriver/downloads
    driver = webdriver.Chrome()

    driver.get(URL)

    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@id="flow-home"]')
    )
    print(f"Element found:  {element_present}")
    WebDriverWait(driver, timeout=60 * 60).until(element_present)

    cookies = driver.get_cookies()
    auth_token = next(
        (cookie["value"] for cookie in cookies if cookie["name"] == COOKIE_NAME), None
    )

    print(f"Auth token: {auth_token}")

    # Cache the auth_token if caching is enabled
    if use_cache:
        utils.cache_data("auth_token", auth_token)

    driver.quit()

    return auth_token
