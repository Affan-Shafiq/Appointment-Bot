from user import user
from selenium import webdriver
import yaml
import time

# Load configuration from YAML file
conf = yaml.load(open('detail.yml'), Loader=yaml.FullLoader)

# Extract users from the YAML file
users = conf['users']

# Initialize Chrome driver
driver = webdriver.Chrome()


# Function to check if the appointment booking was successful
def appointment_successful():
    # You can define your own logic here to determine whether the booking was successful.
    # This could be based on page feedback, URL change, or a success message.
    success_message = "Booking confirmed"
    return success_message in driver.page_source


# Retry logic for booking appointments
def attempt_booking(user_data, max_retries=3):
    email = user_data['email']
    password = user_data['password']
    first_name = user_data['firstName']
    last_name = user_data['lastName']

    for attempt in range(max_retries):
        try:
            print(f"Attempting booking for {email} (Attempt {attempt + 1}/{max_retries})")

            # Create an instance of User class
            u = user(first_name, last_name, email, password, driver)

            # Log in
            u.user_login(url="https://blsitalypakistan.com/account/login")

            # Book the appointment
            u.appointment_booking(url="https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")

            # Check if booking was successful
            if appointment_successful():
                print(f"Appointment successfully booked for {email}")
                return True  # Return success
            else:
                print(f"Appointment booking failed for {email}. Retrying...")

        except Exception as e:
            print(f"Error occurred during booking for {email}: {str(e)}")

        time.sleep(5)  # Wait before retrying

    # If all retries fail, return False
    return False


# Main logic to handle sequential user login and appointment booking
for i, user_data in enumerate(users):
    print(f"Processing user {i + 1}/{len(users)}: {user_data['email']}")

    if i == 0:  # First user should try until success or max retries are reached
        success = attempt_booking(user_data)
        if not success:
            print("First user failed to book an appointment after retries. Exiting.")
            break  # Exit if the first user failed to book an appointment

    else:
        success = attempt_booking(user_data)
        if not success:
            print(f"User {user_data['email']} failed to book an appointment. Stopping further logins.")
            break  # Stop further logins if the previous user fails

# Close the browser
driver.quit()
