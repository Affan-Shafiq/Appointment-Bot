from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import yaml
import time

# Load configuration from YAML file
conf = yaml.load(open('detail.yml'), Loader=yaml.FullLoader)
myEmail = conf['user']['email']
myPassword = conf['user']['password']

# Initialize Chrome driver
driver = webdriver.Chrome()  # Make sure ChromeDriver is in PATH or specify the path


def login(url, usernameId, username, passwordId, password, submit_buttonId):
    driver.get(url)

    # Locate and enter the username
    email_input = driver.find_element(By.XPATH, '//input[@type="text"]')
    email_input.send_keys(myEmail)

    # Locate and enter the password
    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(password)

    # Solve captcha manually if required
    input("Solve the captcha and press Enter to continue...")

    # Locate and click submit button
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()
    driver.get("https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")
    time.sleep(2)
    # Locate the dropdown menu by its ID (valCenterLocationId in your case)
    dropdown = driver.find_element(By.ID, "valCenterLocationId")

    # Create a Select object to interact with the dropdown
    select = Select(dropdown)

    # Select the "Islamabad (Pakistan)" option by visible text
    select.select_by_visible_text("Islamabad (Pakistan)")
    time.sleep(1)

    # Locate the dropdown menu by its ID (valCenterLocationTypeId in your case)
    dropdown = driver.find_element(By.ID, "valCenterLocationTypeId")

    # Create a Select object to interact with the dropdown
    select = Select(dropdown)

    # Select the "National - Study" option by visible text
    select.select_by_visible_text("National - Study")
    time.sleep(1)

    # Locate the dropdown menu by its ID (valAppointmentForMembers in your case)
    dropdown = driver.find_element(By.ID, "valAppointmentForMembers")

    # Create a Select object to interact with the dropdown
    select = Select(dropdown)

    # Select the "Appointment Members" option by visible text
    select.select_by_visible_text("Individual")
    time.sleep(1)

    # Date Picking
    date_picker = driver.find_element(By.ID, "valAppointmentDate")
    date_picker.click()

    # Wait for the date picker to load (you may need to adjust the time)
    time.sleep(2)

    # Find all available dates by checking the class 'label-available'
    available_dates = driver.find_elements(By.CLASS_NAME, "label-available")

    # If any available date is found, click the first one
    if available_dates:
        available_dates[0].click()  # Click the first available date
        print("Available date selected.")
    else:
        print("No available dates found.")

    # Keep the browser open by waiting indefinitely or for a specific amount of time
    input("Press Enter to close the browser...")
    # or you can use time.sleep() to wait for a specific time
    # time.sleep(30)


# Call the login function with actual arguments
login("https://blsitalypakistan.com/account/login", "username_input_id", myEmail, "login_password", myPassword, "submitlogin")

# Do not close the driver automatically
driver.quit()
