from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_button(xpath):
    b = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    b.click()
    print(f"clicked button: {xpath}")


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get("https://krisha.kz/")

click_button("//*[@id='region-selected-value']")
click_button("//*[@id='search-form']/div[1]/div[1]/div[5]/div/div/div/div[2]/div[1]/select/option[2]")
driver.implicitly_wait(2)
click_button("/html/body/main/section[1]/form/div[1]/div[1]/div[5]/div/div/div/div[2]/div[2]/a")
click_button("/html/body/main/section[1]/form/div[2]/button[1]")
path_of_x_button = "/html/body/main/section[3]/div/section[1]/section/div[2]/div[1]/div/div[3]/div[1]/div[2]/div/button"
wait = WebDriverWait(driver, 5)

wait.until(EC.presence_of_element_located((By.XPATH, path_of_x_button)))
click_button(path_of_x_button)
xpath_of_block = "/html/body/main/section[3]/div/section[1]"
needed_div = "a-card__descr"
xpath_of_next_button = "/html/body/main/section[3]/div/nav/a[10]/div"
with open("results.txt", "a", encoding="utf-8") as f:
    while EC.presence_of_element_located((By.XPATH, xpath_of_next_button)):
        block = wait.until(EC.presence_of_element_located((By.XPATH, xpath_of_block)))
        elements = block.find_elements(By.XPATH, './/div[@class="a-card__descr"]')

        for element in elements:
            text = element.text.strip().split('\n')
            f.write('\n'.join(text))
            print(text)

        next_button = wait.until(EC.presence_of_element_located((By.XPATH, xpath_of_next_button)))
        next_button.click()
driver.quit()
