import sys, os
import time
import threading
import subprocess
from appium import webdriver

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.touch_action import TouchAction

##what does it means?
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')




desired_cap= {
    "platformName": "Android",
    "deviceName": "R5CN308Z4SE",
    "appPackage":"com.walabot.test",
    "appActivity":"com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
    "app": "C:\\Users\\GuyLeiba\\OneDrive - vayyar.com\\Desktop\\testapp\\my.apk",
    "noReset":True, ##means that app is not reinstalled
    "fullReset":False
}

try:
    driver=webdriver.Remote("http://localhost:4723/wd/hub",desired_cap) ##create session

except Exception as e:
    print(e)
print("bla")

driver.implicitly_wait(40)

##connection proccess
driver.find_element(AppiumBy.ID,"com.walabot.test:id/chooseLastDevice").click() #fast reconnect button
driver.find_element(AppiumBy.ID,"com.walabot.test:id/okButton").click() ##wifi notification button
driver.find_element(AppiumBy.ID,"android:id/button1").click() ##android Op System connect button





##guidence
driver.find_element(AppiumBy.ID,"com.walabot.test:id/calibrateBtn").click() ##calibration button
driver.press_keycode(AndroidKey.BACK)

driver.find_element(AppiumBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView[4]").click()
driver.find_element(AppiumBy.ID,"com.walabot.test:id/startScan").click()

driver.implicitly_wait(120)
time.sleep(30)








if __name__ == "__main__":
    print("success")

