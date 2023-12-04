from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import pyperclip
import time
import pyautogui
import pandas as pd

'''
Set up the variables we intend to use for web scraping (e.g., coordinate positions of the mouse, number of attempt iterations). If you need to determine your
mouse's coordinates, you can execute a very simple block of code, such as:

x, y = pyautogui.position()
print(f"Current mouse coordinates: x = {x}, y = {y}")
'''

x0, y0 = 1115, 203
x1, y1 = 895, 409
x2, y2 = 856, 546
x3, y3 = 1480, 861    

max_its = 7
current_its = 0

'''
Ingest the table you want to read data from. In this particular example, Pandas is reading a df and printing a pre-populated column into a web entry submission
form.
'''

def clientTable():
    client = pd.read_csv('C:/Users/Desktop/Work/Platform Migration/Your_File_Here.csv', index_col = 0)
    return client
client = clientTable()
pd.set_option('display.max_columns', None)
print(client.iloc[0]['Title'])


'''
Initialize the webdriver for chrome, and prepare the arguments for the specific website you need Selenium to navigate to.
'''

def launchBrowser(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver

# URL of the login page
platform_url = 'https://productivity_tool.com/login'

# URL to be pasted
url_to_paste = 'https://productivity_tool.net/software/projects/boards/43'

# Launch the browser 
driver = launchBrowser(platform_url)

# Wait for the 'username' element to be present
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'username'))
)

# Email to be used
email = 'youremailhere@domain.com'

# Input the email into the email input field
email_input.send_keys(email)

# Wait for the 'login-submit' button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'login-submit'))
)

# Click the "Continue" button
login_button.click()

# Wait for the 'password' element to be visible
password_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'password'))
)

# Password to be used
password = 'YourSecurePassword123'

# Input the password into the password input field
password_input.send_keys(password)

# Wait for the 'login-submit' button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'login-submit'))
)

# Click the "Continue" button
login_button.click()

'''
This block will vary depending on the platform you're accessing; in my case, I needed to navigate a few additional screens where the ref tag was not
immediately visible, so I used the XPATH of a span tag.
'''

# Wait for the button to be clickable
platform_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="start-product__..."]'))
)

# Click the button
platform_button.click()

# Pass through to the MPS Homepage
mps_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="..."]'))
)

# Click 
mps_btn.click()


'''
This may be unnecessary, but because Selenium is fragile, we can set a max number of attempts and force the program to stop as opposed to bombarding the 
system.

max_attempts = 3
attempts = 0

while attempts < max_attempts:
    try:
        newticket_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="createItem"]'))
        )
        newticket_btn.click()
        break
    except StaleElementReferenceException:
        # If the element is stale, re-locate the element
        attempts += 1
        continue

if attempts == max_attempts:
    print("Maximum attempts reached. Element could not be clicked.")'''


'''
This is the core of our process; we simply create a for loop that is going to:
1) Read and assign rows to be iterated on based on our original df.
2) Tell Selenium exactly which coordinates we need it to navigate to, and when to left click to progress through the webpage. 
3) Once we've determined exactly which coordinates pertain to the 'fill-in' part of our webpage, we then tell Selenium to paste data from our iterated row.
4) The loop will continue for as many rows as we need to iterate -- in this case, it was 369 -- and then it will shut itself off.
'''

for index in range(369, len(client)):
    row = client.iloc[index]
    title = row['Title']
    descr = row['Description']

    # Increment the iteration counter
    current_its += 1

    # Implement break logic
    if current_its > 378:
        break

    # Wait for a short duration
    time.sleep(2.5)
    
    # Move the mouse to Selected Location
    pyautogui.moveTo(x0, y0, duration=0.2)
    pyautogui.mouseDown()
    pyautogui.mouseUp()

    # Wait for a short duration
    time.sleep(2.5)
    
    # Move the mouse to Issue Type
    pyautogui.moveTo(x1, y1, duration=0.2)

    # Wait for a short duration
    time.sleep(2)

    # Left click down and up
    pyautogui.mouseDown()
    pyautogui.mouseUp()

    # Wait for a short duration
    time.sleep(2)

    # Move the mouse to the Migration Issue
    pyautogui.moveTo(x2, y2, duration=0.2)

    # Left click down and up
    pyautogui.mouseDown()
    pyautogui.mouseUp()

    # Wait for a short duration
    time.sleep(2)

    # Tab four times
    for _ in range(5):
        pyautogui.press('tab')

    # Copy and paste in the summary
    pyautogui.write(title)

    # Wait for a short duration
    time.sleep(2)

    # Tab nine times
    for _ in range(9):
        pyautogui.press('tab')

    # Copy and paste in the summary
    pyautogui.write(descr)

    # Wait for a short duration
    time.sleep(2)

    # Move the mouse to a separate Selected Location
    pyautogui.moveTo(x3, y3, duration=0.2)

    # Left click down and up
    pyautogui.mouseDown()
    pyautogui.mouseUp()

    # Wait for a short duration
    time.sleep(2.5)


# Add a delay to keep the browser open for 5 seconds
input("Press Enter to close the browser...")


# Close the browser
driver.quit()

