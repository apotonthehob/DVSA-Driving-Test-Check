"""
For personal use
Checkinng for cancellations at the centre booked
"""


from selenium import webdriver
import time
import random
import winsound
from datetime import datetime, timedelta
import sys
from selenium.common.exceptions import NoSuchElementException

details = {
    'Licence': '',  # licence number
    'Booking_Ref': '',  # current test booking reference
    'Test_Centre': '',
    'Test_Date': '2021-10-12', # test date in 'yyyy-mm-yy'
    'Test_Time': '2:32', # test time in 'h:mm'
    'Preferred_Time_1': [820, 930],   # preferred time in 'hmm'
    'Preferred_Time_2': [200, 330]
}
pause = random.randrange(5, 8)  # pause to avoid frequen refresh
attempt_count = 1
bug = "SystemExit" # sound to play when encountering error
complete = "waterdrop.wav" # sound to play when finished


driver = webdriver.Chrome('d:\Downloads\chromedriver_win32\chromedriver.exe')
# open the test booking management website
driver.get('https://driverpracticaltest.dvsa.gov.uk/login')
time.sleep(pause)
step = 0    # breaking down the steps 

def counting(sleep_count, step):
    while True:
        time.sleep(5)
        sleep_count = sleep_count + 1
        if sleep_count > 24:
            winsound.PlaySound(bug, winsound.SND_ALIAS)
            print('Current step:', step)
            user = int(input('Step'))
            step = user
        break
    return sleep_count, step


# Login
while True and step == 0:
    if "Enter details below to access your booking" in driver.find_element_by_id("main").get_attribute(
            'innerHTML'):
        time.sleep(pause)
        # login with current test details
        driver.find_element_by_id("driving-licence-number").send_keys(details["Licence"])
        time.sleep(pause)
        driver.find_element_by_id("application-reference-number").send_keys(details["Booking_Ref"])
        time.sleep(pause)
        driver.find_element_by_id("booking-login").click()
        print("Login Successful")
        time.sleep(pause)
        step = 1
        break

    else:
        sleep_count = 0
        print('Start counting')
        while "Enter details below" not in driver.find_element_by_id("main").get_attribute('innerHTML'):
            counting(sleep_count, step)

while True:
    try:
        # Select change centre
        while True and step == 1:
            if "View booking" in driver.find_element_by_id("main").get_attribute(
                    'innerHTML'):
                time.sleep(pause)
                driver.find_element_by_id("test-centre-change").click()
                if "Test centre" in driver.find_element_by_id("main").get_attribute('innerHTML'):
                    step = 2
                    break

            elif "chosen-test-centre" in driver.find_element_by_id("main").get_attribute('innerHTML'):
                driver.find_element_by_id("change-test-centre").click()
                if "Test centre" in driver.find_element_by_id("main").get_attribute('innerHTML'):
                    step = 2
                    break

            else:
                sleep_count = 0
                while "View booking" not in driver.find_element_by_id("main").get_attribute('innerHTML'):
                    time.sleep(5)
                    sleep_count = sleep_count + 1
                    if attempt_count > 24:
                        winsound.PlaySound(bug, winsound.SND_ALIAS)
                        print('Current step:', step)
                        user = int(input('Step'))
                        step = user
                        break

        # Select centre
        while True and step == 2:
            if "Test centre" in driver.find_element_by_id("main").get_attribute(
                            'innerHTML'):
                time.sleep(pause)
                driver.find_element_by_id("test-centres-input")
                time.sleep(pause)
                driver.find_element_by_id("test-centres-submit").click()
                time.sleep(pause)
                # select first centre
                results_container = driver.find_element_by_class_name("test-centre-results")
                test_centre = results_container.find_element_by_xpath(".//a")
                test_centre.click()
                print("Change Select Successful")
                step = 3
                break

            else:
                sleep_count = 0
                while "Test centre" not in driver.find_element_by_id("main").get_attribute('innerHTML'):
                    time.sleep(5)
                    sleep_count = sleep_count + 1
                    if attempt_count > 24:
                        winsound.PlaySound(bug, winsound.SND_ALIAS)
                        print('Current step:', step)
                        user = int(input('Step'))
                        step = user
                        break

        # check if any slot available
        while True and step == 3:
            print(attempt_count, "attempt:")
            attempt_count += 1
            if "There are no tests available that meet your request" in driver.find_element_by_id("main").get_attribute(
                    'innerHTML'):
                f_time = datetime.now() + timedelta(minutes=pause)
                print("No test available. Try again in ", pause, 'minutes at:', f_time)
                time.sleep(pause*60)
                # try again
                step = 2
            elif "chosen-test-centre" not in driver.find_element_by_id("main").get_attribute('innerHTML'):
                sleep_count = 0
                while "chosen-test-centre" not in driver.find_element_by_id("main").get_attribute('innerHTML'):
                    time.sleep(5)
                    sleep_count = sleep_count + 1
                    if attempt_count > 24:
                        winsound.PlaySound(bug, winsound.SND_ALIAS)
                        print('Current step:', step)
                        user = int(input('Step:'))
                        step = user
                        break

            else:
                print("Test available, checking dates...")
                date_time = {}
                # if slot available, check date and time
                minDate = int(details["Test_Date"].replace('-', ''))
                test_time = int(details['Test_Time'].replace(':', ''))
                available_slots = driver.find_element_by_class_name("SlotPicker-days")
                slots = available_slots.find_elements_by_xpath(".//li")  # finding all available slots
                # analysing dates and time
                for d in slots:
                    if '--unavailable' not in d.get_attribute('class'):
                        time_list = []
                        date = d.get_attribute('id')[5:]
                        s_date = int(date.replace('-', ''))
                        if s_date <= minDate:
                            # print(date)
                            times = d.find_elements_by_class_name('SlotPicker-time')
                            for i in times:
                                t = i.get_attribute('innerHTML')
                                t_n = int(t[:-2].replace(':', ''))
                                if s_date == minDate and test_time == t_n:
                                    continue
                                elif int(details['Preferred_Time_1'][0]) <= t_n <= int(details['Preferred_Time_1'][1]) \
                                        or int(details['Preferred_Time_2'][0]) <= t_n <= int(details['Preferred_Time_2'][1]):
                                    # print(details['Preferred_Time_1'][0], details['Preferred_Time_1'][1],
                                    #       details['Preferred_Time_2'][0], details['Preferred_Time_2'][1])
                                    # print(t)
                                    time_list.append(t)
                        if len(time_list) > 0:
                            date_time[date] = time_list
                            # print(time_list)
                            # print(date_time)
                    # if date and time available, notify the user and print date and time
                if len(date_time) > 0:
                    winsound.PlaySound(complete, winsound.SND_ALIAS)
                    print('Availability:')
                    for key, value in date_time.items():
                        print(key, ':', value)
                    user = int(input('Step(looping again is 1):'))
                    step = user
                    wait = int(input('Try again in minutes:'))
                    time.sleep(wait * 60)
                    f_time = datetime.now() + timedelta(minutes=wait)
                    print("Try again in ", wait, 'minutes at:', f_time)
                else:
                    # try again
                    step = 1
                    f_time = datetime.now() + timedelta(minutes=pause)
                    print("No target slot find. Try again in ", pause, 'minutes at:', f_time)
                    time.sleep(pause * 60)
            break
    except Exception as e:
        winsound.PlaySound(bug, winsound.SND_ALIAS)
        print(e)
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print('Current step:', step)
        user = int(input('Step (looping again is 1):'))
        step = user
