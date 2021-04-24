from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import smtplib

def watchZipCode(fromEmail, fromEmailPass):
    driver = webdriver.Chrome()
    while True:
        driver.get("https://mychart.whhs.com/mychart/covid19#/")

        time.sleep(2)
        btn1 = driver.find_element_by_css_selector('a.btn.btn-lg.btn-primary')
        btn1.click()

        time.sleep(2)
        driver.get("https://mychart.whhs.com/mychart/covid19#/triage")

        # Radio button selection
        answer_list = ["Answer_0", "Answer_1", "Answer_1", "Answer_1", "Answer_1", "Answer_0"]
        for ans in answer_list:
            element = driver.find_element_by_id(ans);
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            status = driver.find_element_by_id(ans).is_selected();
            response = driver.find_element_by_xpath('//*[@id="TriageQuestionCard"]/div[2]/div[2]/a')
            response.click()

        # Navigate to Appointment selection page
        time.sleep(2)
        btn2 = driver.find_element_by_xpath('//*[@id="ResultsCard"]/div[3]/div/div')
        btn2.click()

        # Get status from Appointment selection page
        time.sleep(8)
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        textInMail = driver.find_element_by_tag_name('body').text


        # Validate appointment availablity and send mail if available
        now = datetime.now()
        present_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        errorMessage = "Sorry, we couldn't find any open appointments."
        print('Time ' + present_time, end = '')

        time.sleep(2)
        if textInMail ==  errorMessage :
            print('  Skip sending mail: ' + textInMail)
        else :
            # Send status mail
            time.sleep(2)
            print(textInMail)
            message = "APPOINTMENT FOUND! Message: \n"+textInMail + "\nTime: " + present_time
            sendText(fromEmail, fromEmailPass, message)

        time.sleep(600)

def sendText(fromEmail, fromEmailPass, message):

    Subject = 'Subject: Washington Hospital Vaccine available :\n\n'
    toMail1 = 'mail1@gmail.com'
    toMail2 = 'mail2@gmail.com'
    footer = '- Test'  # add test footer
    conn = smtplib.SMTP_SSL(host="smtp.mail.yahoo.com", port=465)
    conn.login(fromEmail, fromEmailPass)
    conn.sendmail(fromEmail, toMail1, Subject + message)
    conn.sendmail(fromEmail, toMail2, Subject + message)
    conn.quit()


if __name__ == "__main__":
    watchZipCode("mail@yahoo.co.in",  "mail_pw")
