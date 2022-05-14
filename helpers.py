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



def main():
    pass
if __name__ == "__main__":
    main()

def main_session(app_package, apk_path, choosen_folder,devlogname):
    try:
        ANDROID_BASE_CAPS=get_base_caps(app_package,apk_path)
        driver = webdriver.Remote("http://localhost:4723/wd/hub", ANDROID_BASE_CAPS)  ##create session
        driver.implicitly_wait(30)
        guidence_nav(driver,app_package)
        driver.implicitly_wait(120)
        time.sleep(20)
        status=fin(driver,app_package,choosen_folder,devlogname)
        return status
    except Exception as e:
        return e


def guidence_nav(driver,app_package):

    ##Draft!

    driver.find_element(AppiumBy.ID, "{pack}:id/chooseLastDevice".format(pack=app_package)).click()  # fast reconnect button
    driver.find_element(AppiumBy.ID, "{pack}:id/okButton".format(pack=app_package)).click()  ##wifi notification button
    driver.find_element(AppiumBy.ID, "android:id/button1").click()  ##android Op System connect button
    driver.find_element(AppiumBy.ID, "{pack}:id/done".format(pack=app_package)).click()  ##done btn
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


def name_validator(devlogname):
    if ".txt" in devlogname:
        return devlogname
    else:
        return devlogname+".txt"

def pull_devlog(app_package, choosen_folder,devlog):

    ###if no file name was entered
    if devlog:
        choosen_folder = choosen_folder + "\\" + devlog
        adb_pullcommand = "adb pull /sdcard/Android/data/{pack}/files/devlog.txt {folder}".format(pack=app_package,
                                                                                                  folder=choosen_folder)
    else:
        adb_pullcommand = "adb pull /sdcard/Android/data/{pack}/files/devlog.txt {folder}".format(pack=app_package,folder=choosen_folder)

    try:
        out = check_output(adb_pullcommand.split())
        if "1 file pulled" in str(out):
            return "Process Done With No Errors"
        else:
            return "No files"
    except Exception as e:
        return "Error with pulling the file "+str(e)

def delete_devlog(app_package):

    adb_del_command = "adb shell rm /sdcard/Android/data/{pack}/files/devlog.txt".format(pack=app_package)
    subprocess.call(adb_del_command, shell=True)


def fin(driver,app_package,choosen_folder,devlog):

    new_name=name_validator(devlog)
    status=pull_devlog(app_package, choosen_folder,new_name)  ##extractdevlog
    delete_devlog(app_package)  ##deletedevlog
    driver.close_app()
    driver.quit()
    return status

def get_base_caps(app_package,apk_path):

    ANDROID_BASE_CAPS= {
        "platformName": "Android",
        "deviceName": "R5CN308Z4SE",
        "appPackage": app_package,
        "appActivity":"com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
        "app": apk_path,
        "noReset":True, ##means that app is not reinstalled
        "fullReset":False
    }
    return ANDROID_BASE_CAPS


def package_setter(compare_str):
    if compare_str == "Dev":
        return "com.walabot.test"
    elif compare_str == "Production":
        return "com.walabot.vayyar.ai.plumbing"
    else:
        raise AttributeError


##needs more work with regex

def adb_device():
    try:
        adb_ouput = check_output(["adb", "devices"])
        print(adb_ouput)
    except CalledProcessError as e:
        print(e.returncode)



#
# apk_package="com.walabot.test"
# apk_path="C:\\Users\\GuyLeiba\\OneDrive - vayyar.com\\Desktop\\testapp\\my.apk"
# folder=r'C:\Users\GuyLeiba\OneDrive - vayyar.com\Desktop\Testing Fr_test'
# error=helpers.main(apk_package,apk_path,folder)
#

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

