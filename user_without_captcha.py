# User class will hold all the data about a user and will be used in test_without_captcha.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import requests

class user:
    def __init__(self, first_name, last_name, email, password, card_num, driver):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.card_num = card_num
        self.driver = driver

    def user_login(self, url):
        self.driver.get(url)

        # Locate and enter the username
        email_input = self.driver.find_element(By.XPATH, '//input[@type="text"]')
        email_input.send_keys(self.email)

        # Locate and enter the password
        password_input = self.driver.find_element(By.XPATH, '//input[@type="password"]')
        password_input.send_keys(self.password)

        # Manual Captcha Solving
        print("Please solve the CAPTCHA manually.")
        input("After solving the CAPTCHA, press Enter to continue...")

        # Locate and click the submit button
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

    def appointment_booking(self, url):
        self.driver.get(url)
        time.sleep(1)

        try:
            # Locate the dropdown menu by its ID (valCenterLocationId in this case)
            dropdown = self.driver.find_element(By.ID, "valCenterLocationId")
        except:
            # Logout if the dropdown is not found
            self.driver.get('https://blsitalypakistan.com/account/logout')
            time.sleep(2)
            return False

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "Islamabad (Pakistan)" option by visible text
        select.select_by_visible_text("Islamabad (Pakistan)")
        time.sleep(1)

        # Locate the dropdown menu by its ID (valCenterLocationTypeId in this case)
        dropdown = self.driver.find_element(By.ID, "valCenterLocationTypeId")

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "National - Study" option by visible text
        select.select_by_visible_text("National - Study")
        time.sleep(1)

        # Locate the dropdown menu by its ID (valAppointmentForMembers in this case)
        dropdown = self.driver.find_element(By.ID, "valAppointmentForMembers")

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "Appointment Members" option by visible text
        select.select_by_visible_text("Individual")
        time.sleep(1)

        # Date Picking
        date_picker = self.driver.find_element(By.ID, "valAppointmentDate")
        date_picker.click()

        # Wait for the date picker to load
        time.sleep(2)

        # Find all elements with class 'label-available'
        all_labels = self.driver.find_elements(By.CLASS_NAME, "label-available")

        # Filter and click the valid appointment date
        for label in all_labels:
            # Check the data-original-title attribute to determine if it's an appointment date
            tooltip = label.get_attribute("data-original-title")
            if tooltip != "Appointment Available":
                label.click()
                print("Available date selected.")
                break
            else:
                print("No available dates found.")
                # Logout
                self.driver.get('https://blsitalypakistan.com/account/logout')
                time.sleep(2)
                return False

        # Manual Captcha Solving
        print("Please solve the CAPTCHA manually.")
        input("After solving the CAPTCHA, press Enter to continue...")

        # Locate the dropdown menu by its ID (valAppointmentType in this case)
        dropdown = self.driver.find_element(By.ID, "valAppointmentType")

        # Create a Select object to interact with the dropdown
        select = Select(dropdown)

        # Select the "- Normal -" option by visible text
        select.select_by_visible_text("- Normal -")
        time.sleep(1)

        # Now, handling the time slot selection
        # Locate the normal slots dropdown
        normal_time_slot_dropdown = self.driver.find_element(By.CLASS_NAME, "form-control.time_slot_lists.normal_slots")

        # Create a Select object for normal time slots
        select_normal_slot = Select(normal_time_slot_dropdown)

        # Check for available options in the normal slots dropdown
        normal_options = select_normal_slot.options

        # If there are any available options
        if len(normal_options) > 1:
            select_normal_slot.select_by_index(1)
            print("First available normal time slot selected.")
        else:
            print("No available normal time slots.")

        time.sleep(1)

        # Locate and enter the first_name
        first_name_input = self.driver.find_element(By.NAME, 'valApplicant[1][first_name]')
        first_name_input.send_keys(self.first_name)

        # Locate and enter the last_name
        last_name_input = self.driver.find_element(By.NAME, 'valApplicant[1][last_name]')
        last_name_input.send_keys(self.last_name)

        # Handling the Checkbox
        checkbox = self.driver.find_element(By.ID, 'agree')

        # Check if the checkbox is not already selected
        if not checkbox.is_selected():
            checkbox.click()

        # Manual Captcha Solving
        print("Please solve the CAPTCHA manually.")
        input("After solving the CAPTCHA, press Enter to continue...")

        # Locate and click the submit button
        submit_button = self.driver.find_element(By.ID, 'valBookNows')
        submit_button.click()

        # At this point, the page redirects to the payment page
        # Now, let's handle the payment page
        time.sleep(5)

        # Fill in card details
        card_number_input = self.driver.find_element(By.ID, 'cardNumber')
        card_number_input.send_keys(self.card_num)

        # Select expiry month from dropdown
        expiry_month_dropdown = self.driver.find_element(By.ID, 'expiryMonth')
        select_month = Select(expiry_month_dropdown)
        select_month.select_by_visible_text('September')

        # Select expiry year from dropdown
        expiry_year_dropdown = self.driver.find_element(By.ID, 'expiryYear')
        select_year = Select(expiry_year_dropdown)
        select_year.select_by_visible_text('2028')

        # Enter CVC
        cvc_input = self.driver.find_element(By.ID, 'cvc')
        cvc_input.send_keys('794')

        # Click the Pay button
        pay_button = self.driver.find_element(By.ID, 'payButton')
        pay_button.click()

        # Wait for the payment to process
        time.sleep(5)

        # Logout
        self.driver.get('https://blsitalypakistan.com/account/logout')
        time.sleep(2)

        # Return to confirm application status
        return True

    def solve_captcha(self, site_key, url):
        # Function to solve Google reCAPTCHA using 2Captcha API
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
            time.sleep(2)  # Waiting 2 seconds before checking the result
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

    def solve_img_captcha(self, image_url):
        # Step 1: Send captcha image to 2Captcha for solving
        captcha_image_response = requests.get(image_url)

        API_KEY = '9e4ae0036f75fa977a5976d3985b48df'

        # Save captcha image locally (optional but useful for debugging)
        with open("captcha_image.jpg", "wb") as file:
            file.write(captcha_image_response.content)

        # Step 2: Send captcha to 2Captcha
        files = {
            'file': open('captcha_image.jpg', 'rb')
        }

        captcha_data = {
            'key': API_KEY,
            'method': 'post',
            'file': 'captcha_image.jpg',
            'json': 1  # Get JSON response
        }

        captcha_response = requests.post('http://2captcha.com/in.php', files=files, data=captcha_data)
        captcha_id = captcha_response.json()['request']

        # Step 3: Polling the 2Captcha service for the solution
        fetch_url = f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1'

        print('Waiting for captcha solution...')
        for _ in range(20):  # Poll for the solution up to 20 times (with 5-second intervals)
            time.sleep(5)
            result_response = requests.get(fetch_url)
            result_json = result_response.json()

            if result_json['status'] == 1:
                # If captcha is solved
                return result_json['request']

        return None  # Return None if the captcha was not solved in time