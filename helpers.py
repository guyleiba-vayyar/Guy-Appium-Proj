import os
import sys
from selenium.common.exceptions import InvalidSessionIdException
from datetime import datetime
import sys, os
import time
import threading
import subprocess
from appium import webdriver
from subprocess import call
import traceback
import logging
from subprocess import check_output, CalledProcessError

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.touch_action import TouchAction

def main_session(app_package,apk_path,choosen_folder):

    try:
        ANDROID_BASE_CAPS=get_base_caps(app_package,apk_path)
        driver = webdriver.Remote("http://localhost:4723/wd/hub", ANDROID_BASE_CAPS)  ##create session
        driver.implicitly_wait(10)
        guidence_nav(driver,app_package)
        driver.implicitly_wait(120)
        time.sleep(110)
        __fin(driver,app_package,choosen_folder)
    except Exception as e:
        return e
def guidence_nav(driver,app_package):

    ##Draft!

    driver.find_element(AppiumBy.ID, "{pack}:id/chooseLastDevice".format(pack=app_package)).click()  # fast reconnect button
    driver.find_element(AppiumBy.ID, "{pack}:id/okButton".format(pack=app_package)).click()  ##wifi notification button
    driver.find_element(AppiumBy.ID, "android:id/button1").click()  ##android Op System connect button
    driver.find_element(AppiumBy.ID, "{pack}:id/calibrateBtn".format(pack=app_package)).click()  ##calibration button
    driver.press_keycode(AndroidKey.BACK)
    temp_string='/hierarchy/android.widget.FrameLayout/' \
                'android.widget.LinearLayout/'\
                'android.widget.FrameLayout/android.widget.RelativeLayout/'\
                'android.widget.RelativeLayout/android.widget.RelativeLayout/'\
                'android.widget.ImageView[4]'

    driver.find_element(AppiumBy.XPATH,temp_string).click()
    driver.find_element(AppiumBy.ID, "{pack}:id/startScan".format(pack=app_package)).click()


    ##connection proccess !!working!!

    # driver.find_element(AppiumBy.ID, "com.walabot.test:id/chooseLastDevice").click()  # fast reconnect button
    # driver.find_element(AppiumBy.ID, "com.walabot.test:id/okButton").click()  ##wifi notification button
    # driver.find_element(AppiumBy.ID, "android:id/button1").click()  ##android Op System connect button

##need to add devlogname

def _pull_devlog(app_package, choosen_folder):
    adb_pullcommand = "adb pull /sdcard/Android/data/{pack}/files/devlog.txt {folder}".format(pack=app_package,folder=choosen_folder)
    subprocess.call(adb_pullcommand, shell=True)

def _delete_devlog(app_package):

    adb_del_command = "adb shell rm /sdcard/Android/data/{pack}/files/devlog.txt".format(pack=app_package)
    subprocess.call(adb_del_command, shell=True)


def __fin(driver,app_package,choosen_folder):

    _pull_devlog(app_package, choosen_folder)  ##extractdevlog
    _delete_devlog(app_package)  ##deletedevlog
    driver.close_app()
    driver.quit()


def get_base_caps(app_package,apk_path):

    ANDROID_BASE_CAPS= {
        "platformName": "Android",
        "deviceName": "R5CN308Z4SE",
        #"appPackage":"com.walabot.test",
        "appPackage": app_package,
        "appActivity":"com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
        #"app": "C:\\Users\\GuyLeiba\\OneDrive - vayyar.com\\Desktop\\testapp\\my.apk",
        "app": apk_path,
        "noReset":True, ##means that app is not reinstalled
        "fullReset":False
    }
    return ANDROID_BASE_CAPS


##needs more work with regex
def adb_device():
    try:
        adb_ouput = check_output(["adb", "devices"])
        print(adb_ouput)
    except CalledProcessError as e:
        print(e.returncode)

apk_package="com.walabot.test"
apk_path="C:\\Users\\GuyLeiba\\OneDrive - vayyar.com\\Desktop\\testapp\\my.apk"
folder=r'C:\Users\GuyLeiba\OneDrive - vayyar.com\Desktop\Testing Fr_test'
error=main_session(apk_package,apk_path,folder)

# def isappinstalled(driver,desired_package): ##draft
#
#     bool_index=False
#     app_packeges_lst=[] #insert all app packeges that i have
#     app_packeges_lst.append("com.walabot.vayyar.ai.plumbing")
#     for i in range(len(app_packeges_lst)):
#         bool_index=driver.is_app_installed(app_package)
#         if bool_index==True and app_packeges_lst[i]!=desired_package:
#             undesired_packege=app_packeges_lst[i]
#             break
#     return undesired_packege


# def isconnected(driver):
#     threading.Timer(30.0, isconnected).start() # called every minute
#     boolval=driver.find_element(AppiumBy.ID,"com.walabot.test:id/reconnectButton").is_displayed()
#     if boolval:
#         print("Walabot is Disconnected")
#











IOS_BASE_CAPS = {
    'app': os.path.abspath('../apps/TestApp.app.zip'),
    'automationName': 'xcuitest',
    'platformName': 'iOS',
    'platformVersion': os.getenv('IOS_PLATFORM_VERSION') or '12.2',
    'deviceName': os.getenv('IOS_DEVICE_NAME') or 'iPhone 8 Simulator',
    # 'showIOSLog': False,
}


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def take_screenshot_and_logcat(driver, device_logger, calling_request):
    __save_log_type(driver, device_logger, calling_request, 'logcat')


def take_screenshot_and_syslog(driver, device_logger, calling_request):
    __save_log_type(driver, device_logger, calling_request, 'syslog')


def __save_log_type(driver, device_logger, calling_request, type):
    logcat_dir = device_logger.logcat_dir
    screenshot_dir = device_logger.screenshot_dir

    try:
        driver.save_screenshot(os.path.join(screenshot_dir, calling_request + '.png'))
        logcat_data = driver.get_log(type)
    except InvalidSessionIdException:
        logcat_data = ''

    with open(os.path.join(logcat_dir, '{}_{}.log'.format(calling_request, type)), 'w') as logcat_file:
        for data in logcat_data:
            data_string = '%s:  %s\n' % (data['timestamp'], data['message'].encode('utf-8'))
            logcat_file.write(data_string)
