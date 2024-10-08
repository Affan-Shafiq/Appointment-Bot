from user import user
from selenium import webdriver
import yaml
import time

conf = yaml.load(open('detail.yml'), Loader=yaml.FullLoader)
users = conf['users']

# Initialize Chrome driver
driver = webdriver.Chrome()
appointment_status = False

while not appointment_status:
    i = 0
    for user_data in users:
        email = user_data['email']
        password = user_data['password']
        firstName = user_data['firstName']
        lastName = user_data['lastName']
        cardNo = user_data['cardNo']
        u = user(firstName, lastName, email, password, cardNo, driver)
        if i == 0:
            u.user_login(url="https://blsitalypakistan.com/account/login")
            time.sleep(1)
            appointment_status = u.appointment_booking(url="https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")
            if appointment_status:
                i = i + 1
            else:
                break
        else:
            u.user_login(url="https://blsitalypakistan.com/account/login")
            time.sleep(1)
            appointment_status = u.appointment_booking(url="https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")
            if not appointment_status:
                appointment_status = True
                break