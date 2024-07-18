from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime

# File saving
saving_path_root = f"parsing_results/txt/"
result_no = len(os.listdir(saving_path_root))
current_date = datetime.date.today()
current_date = current_date.strftime("%y%m%d")
saving_path = f'{saving_path_root}parsing_result_{current_date}_{result_no}.txt'



# Method for clicking button on a page
def click_button(xpath):
    b = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    b.click()
    print(f"clicked button: {xpath}")


# Set up web driver
options = webdriver.ChromeOptions()
options.add_argument('--headless') # Silent mode, Chrome page doesn't open on screen
driver = webdriver.Chrome(options=options)
driver.get("https://krisha.kz/")  # Get krisha kz



click_button("//*[@id='region-selected-value']")  # choose region button
click_button("//*[@id='search-form']/div[1]/div[1]/div[5]/div/div/div/div[2]/div[1]/select/option[3]") # choose almaty button
# driver.implicitly_wait(2)
click_button("/html/body/main/section[1]/form/div[1]/div[1]/div[5]/div/div/div/div[2]/div[2]/a") # submit button
click_button("/html/body/main/section[1]/form/div[2]/button[1]") # search button
path_of_x_button = "/html/body/main/section[3]/div/section[1]/section/div[2]/div[1]/div/div[3]/div[2]/div[1]/div/button/i" 
wait = WebDriverWait(driver, 10)

# wait.until(EC.presence_of_element_located((By.XPATH, path_of_x_button)))
click_button(path_of_x_button)
xpath_of_block = "/html/body/main/section[3]/div/section[1]"

needed_div = "a-card__descr"
xpath_of_next_button = "/html/body/main/section[3]/div/nav/a[10]/div"
i = 0


with open(saving_path, "a", encoding="utf-8") as f:
    try:
        # EC.presence_of_element_located((By.XPATH, xpath_of_next_button)):
        while i < 1000:
            block = wait.until(EC.presence_of_element_located(
                (By.XPATH, xpath_of_block)))
            elements = block.find_elements(
                By.XPATH, './/div[@class="a-card__descr"]')

            for element in elements:
                text = element.text.strip().split('\n')
                f.write('|'.join(text) + '\n')
                # print(text)

            next_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, xpath_of_next_button)))
            next_button.click()
            i += 1
    finally:
        print(i)
        print(i, file=f)
        f.flush()  # Flush the buffer
        f.close()  # Close the file

driver.quit()
