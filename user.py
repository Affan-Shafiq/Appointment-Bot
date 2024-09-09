# User class will hold all the data about a user and will be used in test.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import requests

class user:
    def __init__(self, first_name, last_name, email, password, driver):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.driver = driver

    def user_login(self, url):
        self.driver.get(url)

        # Locate and enter the username
        email_input = self.driver.find_element(By.XPATH, '//input[@type="text"]')
        email_input.send_keys(self.email)

        # Locate and enter the password
        password_input = self.driver.find_element(By.XPATH, '//input[@type="password"]')
        password_input.send_keys(self.password)

        # Solve reCAPTCHA
        site_key = "6LcVdzUqAAAAAPGbSct68gBCV0Rh3QWAVJdYlMh0"  # Site key from your HTML
        captcha_token = self.solve_captcha(site_key, url)

        # Insert the CAPTCHA token into the hidden g-recaptcha-response field
        self.driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_token}";')

        # Locate and click the submit button
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

    def appointment_booking(self, url):
        self.driver.get("https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")
        time.sleep(1)

        # Locate the dropdown menu by its ID (valCenterLocationId in your case)
        dropdown = self.driver.find_element(By.ID, "valCenterLocationId")

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "Islamabad (Pakistan)" option by visible text
        select.select_by_visible_text("Islamabad (Pakistan)")
        time.sleep(1)

        # Locate the dropdown menu by its ID (valCenterLocationTypeId in your case)
        dropdown = self.driver.find_element(By.ID, "valCenterLocationTypeId")

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "National - Study" option by visible text
        select.select_by_visible_text("National - Study")
        time.sleep(1)

        # Locate the dropdown menu by its ID (valAppointmentForMembers in your case)
        dropdown = self.driver.find_element(By.ID, "valAppointmentForMembers")

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "Appointment Members" option by visible text
        select.select_by_visible_text("Individual")
        time.sleep(1)

        # Date Picking
        date_picker = self.driver.find_element(By.ID, "valAppointmentDate")
        date_picker.click()

        # Wait for the date picker to load (you may need to adjust the time)
        time.sleep(2)

        # Find all available dates by checking the class 'label-available'
        available_dates = self.driver.find_elements(By.CLASS_NAME, "label-available")

        # If any available date is found, click the first one
        if available_dates:
            available_dates[0].click()  # Click the first available date
            print("Available date selected.")
        else:
            print("No available dates found.")
        # Return something to confirm application status

    def solve_captcha(self, site_key, url):
        """
        Function to solve Google reCAPTCHA using 2Captcha API
        """
        API_KEY = '9e4ae0036f75fa977a5976d3985b48df'
        # Send captcha solving request to 2Captcha
        captcha_id = requests.post(
            "http://2captcha.com/in.php",
            data={
                'key': API_KEY,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': url,
                'json': 1
            }
        ).json()

        captcha_id = captcha_id['request']

        # Wait for the result
        result = None
        while True:
            time.sleep(5)  # Waiting 5 seconds before checking the result
            result = requests.get(
                f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
            ).json()
            if result['status'] == 1:
                break
            elif result['status'] == 0 and result['request'] == "CAPCHA_NOT_READY":
                print("Waiting for CAPTCHA to be solved...")
            else:
                raise Exception(f"Error solving CAPTCHA: {result['request']}")

        return result['request']