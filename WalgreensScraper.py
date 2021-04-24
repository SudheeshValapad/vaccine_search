from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import smtplib


def watchZipCode(zips, fromEmail, fromEmailPass, loginId, loginPw):

    driver = webdriver.Chrome()
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19")
    btn = driver.find_element_by_css_selector('span.btn.btn__blue')
    btn.click()
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19/location-screening")
    while True:

        for zipCode in zips:
            driver.get("https://www.walgreens.com/findcare/vaccination/covid-19/location-screening")
            element = driver.find_element_by_id("inputLocation")
            element.clear()
            element.send_keys(zipCode)
            button = driver.find_element_by_css_selector("button.btn")
            button.click()

            time.sleep(3)
            alertElement = getAlertElement(driver)
            aptFound = alertElement.text == "Appointments available!"
            if aptFound:
                now = datetime.now()
                present_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                print('Time ' + present_time, end='')
                print("  ======================APPOINTMENT FOUND! ZIP CODE: "+zipCode+"  ======================")
                message = "APPOINTMENT FOUND! ZIP CODE: " + zipCode + "\nTime: " + present_time
                # sendText(fromEmail, fromEmailPass, message)

                btn = driver.find_element_by_css_selector('span.btn.btn__blue')
                btn.click()
                time.sleep(4)

                # Log In to account
                try:
                    element = driver.find_element_by_id("user_name")
                    element.clear()
                    element.send_keys(loginId)
                    element = driver.find_element_by_id("user_password")
                    element.clear()
                    element.send_keys(loginPw)
                    btn = driver.find_element_by_css_selector('button.btn.btn__blue.btn-block.mb20')
                    btn.click()
                    time.sleep(5)
                except:
                    print("Exception happened1")
                    time.sleep(2)

                # Complete form for eligibility in California
                # Radio button selection & eligibility check
                try:
                    element1 = driver.find_element_by_id("sq_100i_4")
                    driver.execute_script("arguments[0].click();", element1)
                    element2 = driver.find_element_by_id("eligibility-check")
                    driver.execute_script("arguments[0].click();", element2)
                    btn = driver.find_element_by_css_selector('input.sv_complete_btn')
                    btn.click()
                    time.sleep(6)
                except:
                    print("Exception happened2")
                    # Keeping your account safe
                    element = driver.find_element_by_id("radio-security")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(2)
                    btn = driver.find_element_by_css_selector('button.btn.btn__blue.btn-block-mob')
                    btn.click()
                    time.sleep(2)

                    element = driver.find_element_by_id("secQues")
                    element.send_keys("sreejith")
                    time.sleep(1)
                    btn = driver.find_element_by_css_selector('button.btn.btn__blue.btn-block-mob')
                    btn.click()
                    time.sleep(2)
                    #------------

                    element1 = driver.find_element_by_id("sq_100i_4")
                    driver.execute_script("arguments[0].click();", element1)
                    element2 = driver.find_element_by_id("eligibility-check")
                    driver.execute_script("arguments[0].click();", element2)
                    btn = driver.find_element_by_css_selector('input.sv_complete_btn')
                    btn.click()
                    time.sleep(6)
                    print("Recovering...")

                # COVID-19 Vaccination Screening
                element1 = driver.find_element_by_id("sq_100i_1")
                driver.execute_script("arguments[0].click();", element1)
                element2 = driver.find_element_by_id("sq_102i_1")
                driver.execute_script("arguments[0].click();", element2)
                element1 = driver.find_element_by_id("sq_103i_1")
                driver.execute_script("arguments[0].click();", element1)
                element2 = driver.find_element_by_id("sq_104i_0")
                driver.execute_script("arguments[0].click();", element2)
                btn = driver.find_element_by_css_selector('input.sv_complete_btn')
                btn.click()
                time.sleep(3)

                btn = driver.find_element_by_css_selector('a.btn.btn__blue.button-agree')
                btn.click()
                time.sleep(2)



                # Schedule your vaccination
                element1 = driver.find_element_by_id("dose1")
                driver.execute_script("arguments[0].click();", element1)
                time.sleep(6)
                btn = driver.find_element_by_css_selector('button.btn.btn__blue.btn__full-width')
                btn.click()
                time.sleep(3)

                # FremontFound = "Fremont"
                FremontFound = 'class="wag-mob-txtbold">94538'
                if (FremontFound in driver.page_source):
                    print("Yes! At Fremont")
                    sendText(fromEmail, fromEmailPass, message)
                    time.sleep(600)
                else:
                    print("Not at Fremont")
                    time.sleep(323)

            elif not aptFound:
                now = datetime.now()
                present_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                print('Time ' + present_time, end='')
                print(" No appointments available")
                time.sleep(302)
            else:
                print("Bug! Check source code")
                time.sleep(302)


def getAlertElement(driver):
    while True:
        try:
            alertElement = driver.find_element_by_css_selector('div.alert__text-contain')
            return alertElement
        except NoSuchElementException:
            time.sleep(0.5)


def sendText(fromEmail, fromEmailPass, message):
    Subject = 'Subject: Fremont Walgreens have vaccine !\n\n'
    toMail1 = 'mail1@gmail.com'
    toMail2 = 'mail2@gmail.com'
    conn = smtplib.SMTP_SSL(host="smtp.mail.yahoo.com", port=465)
    conn.login(fromEmail, fromEmailPass)
    conn.sendmail(fromEmail, toMail1, Subject + message)
    conn.sendmail(fromEmail, toMail2, Subject + message)
    conn.quit()


if __name__ == "__main__":
    zips = ["94538", "94538"]
    watchZipCode(zips, "mail@yahoo.co.in",  "mail_password", "walgreens_login_id",  "walgreenlogin_pw",)
