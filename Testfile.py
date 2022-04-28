from appium import webdriver
import time
import threading

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.extensions.android.nativekey import AndroidKey


def isappinstalled(driver,desired_package): ##draft

    bool_index=False
    app_packeges_lst=[] #insert all app packeges that i have
    app_packeges_lst.append("com.walabot.vayyar.ai.plumbing")
    for i in range(len(app_packeges_lst)):
        bool_index=driver.is_app_installed(app_package)
        if bool_index==True and app_packeges_lst[i]!=desired_package:
            undesired_packege=app_packeges_lst[i]
            break
    return undesired_packege


def isconnected(driver):
    threading.Timer(30.0, isconnected).start() # called every minute
    boolval=driver.find_element(AppiumBy.ID,"com.walabot.test:id/reconnectButton").is_displayed()
    if boolval:
        print("Walabot is Disconnected")


# app_package="com.walabot.test"
# app_activity="com.walabot.vayyar.ai.plumbing.presentation.MainActivity"
# app_apk_location="C:\\Users\\GuyLeiba\\OneDrive - vayyar.com\\Desktop\\testapp\\my.apk"


desired_cap= {
    "platformName": "Android",
    "deviceName": "R5CN308Z4SE",
    "appPackage":"com.walabot.test",
    "appActivity":"com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
    "app": "C:\\Users\\GuyLeiba\\OneDrive - vayyar.com\\Desktop\\testapp\\my.apk",
    "noReset":True, ##means that app is not reinstalled
    "fullReset":False
}


driver=webdriver.Remote("http://localhost:4723/wd/hub",desired_cap) ##create session

driver.implicitly_wait(30)

##connection proccess
driver.find_element(AppiumBy.ID,"com.walabot.test:id/chooseLastDevice").click() #fast reconnect button
driver.find_element(AppiumBy.ID,"com.walabot.test:id/okButton").click() ##wifi notification button
driver.find_element(AppiumBy.ID,"android:id/button1").click() ##android Op System connect button

##guidence

# if driver.find_element(AppiumBy.ID,"com.walabot.test:id/calibrateBtn").is_displayed():
#     driver.find_element(AppiumBy.ID,"com.walabot.test:id/calibrateBtn").click() ##calibration button
# else:
#     driver.find_element(AppiumBy.ID,"com.walabot.test:id/done").click() ##done button

driver.find_element(AppiumBy.ID,"com.walabot.test:id/calibrateBtn").click() ##calibration button
driver.press_keycode(AndroidKey.BACK)



#isconnected(driver)



#driver.launch_app()

#driver.install_app(app_apk_location)

#driver.start_activity(app_package, app_activity)


# driver.start_activity(app_package, app_activity)
# log_types = driver.log_types
# logs = driver.get_log(log_types[0])
# print(logs)

#devlog_base64 = self.driver.pull_file('This PC\Galaxy S20+ 5G\Phone\Android\data\com.walabot.test\files');

time.sleep(120)
driver.close_app()

driver.quit()
