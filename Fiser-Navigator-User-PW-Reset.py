# This script will reset passwords in Fiserv Navigator.
from ast import Pass
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

# The values stored below will be used. 
eNumber = getpass.getuser()
currentPW = getpass.getpass(prompt='Enter your Password:')
resetUser = input('Enter the employee number of the user who needs a password reset:')
newPW = getpass.getpass(prompt='Enter user temp password:')
while True:
        try:
            siteSelection = int(input("Enter Test region(range=1-8):"))-1
            if siteSelection < 0 or siteSelection > 7 :
                raise ValueError  
            break
        except ValueError:
            print("Invalid entry. Value must be in the range of 1-8.")

# We'll use Microsoft Edge.
driver = webdriver.Edge()

# This will start session in the following url.
t1 = "https://nav1.uat.domain.com/NAV_NAV1151/NAV1151.ASPX"
t2 = "https://nav2.test.domain.com/NAV_NAV1151/NAV1151.ASPX"
t3 = "https://nav3.test.domain.com/NAV_NAV1151/NAV1151.ASPX" 
t4 = "https://nav3.test.domain.com/NAV_NAV1151/NAV1151.ASPX"
t5 = "https://nav5.test.domain.com/NAV_NAV1151/NAV1151.ASPX"
t6 = "https://nav6.test.domain.com/NAV_NAV1151/NAV1151.ASPX"
t7 = "https://nav6.test.domain.com/NAV_NAV1151/NAV1151.ASPX"
t8 = "https://nav6.test.domain.com/NAV_NAV1151/NAV1151.ASPX"
testRegions = [t1, t2, t3, t4, t5, t6, t7, t8]
testRegion = testRegions[siteSelection]

driver.get(testRegion)

# This deals with the dropdown menu in Test 6-8.
if siteSelection > 4:
    if siteSelection == 7:
        chooseRegion = driver.find_element(By.XPATH,"//*[@id='Group']")
        chooseRegion.click()
        chooseRegion.send_keys(Keys.DOWN)
        chooseRegion.send_keys(Keys.DOWN)
        submitRegion = driver.find_element(By.XPATH, "//*[@id='groupSelect']/div[2]/input")
        submitRegion.click()
    elif siteSelection == 6:
        chooseRegion = driver.find_element(By.XPATH,"//*[@id='Group']")
        chooseRegion.click()
        chooseRegion.send_keys(Keys.DOWN)
        submitRegion = driver.find_element(By.XPATH, "//*[@id='groupSelect']/div[2]/input")
        submitRegion.click()
    else:
        submitRegion = driver.find_element(By.XPATH, "//*[@id='groupSelect']/div[2]/input")
        submitRegion.click()
else:
    Pass

# This logs in the administrator who launches the script.  
userID = driver.find_element(By.XPATH,"//*[@id='PrincipalID']")
userID.send_keys(eNumber)
userID.send_keys(Keys.TAB)

userPW = driver.find_element(By.XPATH,"//*[@id='PrincipalPWD']")
userPW.send_keys(currentPW)
userPW.send_keys(Keys.RETURN)

# This will expand Security Control Module.
securityControlModule = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='VerticalNav']/li[28]/a"))
)
securityControlModule.click()

# This will expand On-Line Security.
onlineSecurity = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='VerticalNav']/li[28]/ul/li/a"))
)
onlineSecurity.click()

# This will click the Reset Password button.
resetPW = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Reset Password"))
)
resetPW.click()

# This sends the e-number you entered for the user that needs to be reset. 
driver.switch_to.frame("Main")
userField = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='CodeTextBx']"))
)
userField.send_keys(resetUser)

# This will click the submit button.
submit = driver.find_element(By.XPATH, "//*[@id='ResetPasswordSubmit']")
submit.click()

# This will enter the temp password you set for the user and submit it.
newAccessCodePassword = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.NAME, "AccessPassword"))
)
newAccessCodePassword.send_keys(newPW)
newAccessCodePassword.send_keys(Keys.TAB)
newAccessCodePassword.send_keys(Keys.RETURN)

# Switch out of the iframe and back to the default. 
driver.switch_to.parent_frame()

# This presses the Security Control button near the top of the vertical navigation menu.
securityControl = WebDriverWait(driver,2).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='VerticalNav']/li[3]/a"))  
)
securityControl.click()

# This logs you out.
logOutButton = WebDriverWait(driver,2).until(
    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='VerticalNav']/li[3]/ul/li[1]/a"))
)
logOutButton.click()                          

driver.quit()


