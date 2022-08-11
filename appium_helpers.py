from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException, ElementNotVisibleException
import sys, os
import time
import subprocess
from appium import webdriver
from subprocess import call
import re
from datetime import datetime
from loguru import logger
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey

from Devices_Dict import num_dict, InsideElementError, FlagElementCouldNotFound, ScanInProgress, SignInError, \
    AppiumConnectionError
from server_helpers import Android_Connector


class Tester():

    def __init__(self, value_dict):

        #self.devlog_name = value_dict["devlogname"]

        self.walabot_ssid = re.findall(r'\d{1,3}', value_dict["walabot_ssid"])
        self.app_package = value_dict["app_package"]
        self.device = value_dict["device"]

        self.start_logger()

        """initializing the progress bar"""
        self.device.change_prog_bar(color="white", value=None, message=self.device.device_real_name)

    def start_test(self):
        """
        This is the main function, it starts the appium test and initializes the appium driver
        The for loop creates a unique name for each devlog, based on the number of times the user chose
        to run the test, Helper is num_dict.
        """

        """delay time to over come connectivity issues"""
        time.sleep(self.device.device_number * 10)


        for test_number in range(1, self.device.desired_run_num + 1):

            """Showing the device current test number and logging the run number"""
            self.device.change_prog_bar(
                message=f"{self.device.device_real_name}-{test_number}/{self.device.desired_run_num}     ")
            self.context_logger.info(f"{test_number} Out {self.device.desired_run_num}-Run Started")

            self.start_test_helper(test_number)

            if test_number == self.device.desired_run_num:
                continue
            else:
                """Colling time"""
                time.sleep(self.device.desired_cool_num * 60)

    def start_test_helper(self, current_test_num):
        """
        :param current_test_num:The run number that is currently happen.
        """
        try:
            self.device.change_prog_bar()
            # self.appium_connection(current_test_num)

            android_server = Android_Connector(webdriver, self.app_package, self.device, self.context_logger)
            self.driver = android_server.create_connection(current_test_num)

            if not self.driver:
                self.device.change_prog_bar('red', 100, "Test Failed,Server Down")
                raise AppiumConnectionError

            self.context_logger.success(f"Connection Established With Appium")

            self.driver.implicitly_wait(15)
            """Main navigation function"""
            self.driver.unlock()
            self.app_open_fresh(current_test_num)



        except ScanInProgress:
            """This is not an error, this block of code is expected when 
            everything went well and scan is happening"""
            # self.driver.implicitly_wait(60)
            self.device.change_prog_bar(message="Scan In Progress    ")
            time.sleep(self.device.desired_scan_time)
            android_server.fin(self.driver,current_test_num, True)
            self.device.change_prog_bar(message="Cooling...    ")


            """Error Handling"""

        except AppiumConnectionError:
            self.context_logger.error(f"Test Failed with Connection Error")
            self.device.start_btn.config(state='enabled')
        except NoSuchElementException:
            android_server.fin(self.driver,current_test_num)
            self.context_logger.error(f"Test Failed due to Unfounded Element")
        except InsideElementError:
            android_server.fin(self.driver,current_test_num)
            self.context_logger.error(f"Test Failed due to Unfounded INSIDE Element")
        except SignInError:
            android_server.fin(self.driver,current_test_num)
            self.context_logger.error(
                f"Test Failed,User Name and password doesn't work or couldn't find sign in button")
        except Exception as e:
            android_server.fin(self.driver,current_test_num)
            self.context_logger.error(f"{e}")

    def app_open_fresh(self, current_test_num):
        """
        This function is the main navigation function, it bundles all the flow of the application.
        :return:
        """
        """APP open waiting time"""
        self.driver.implicitly_wait(10)

        """fast reconnect"""
        if current_test_num != 1:
            try:
                self.click_on_flag_element("chooseLastDevice")
                self.flow_from_connection()
            except FlagElementCouldNotFound:
                pass

        """Switch Walabot Screen"""
        try:
            self.driver.implicitly_wait(4)
            self.click_on_flag_element("switchDevice")
            self.click_on_element("walabot_diy_2")
            self.flow_from_choose_walabot()
            self.flow_from_connection()
        except FlagElementCouldNotFound:
            pass

        """Choose Walabot Screen"""
        try:
            self.driver.implicitly_wait(4)
            self.click_on_flag_element("ribbon")
            self.flow_from_choose_walabot()
            self.flow_from_connection()
        except FlagElementCouldNotFound:
            pass

        """In this Block,if Appium can't find something,something is broken."""
        try:
            """Bypassing The two main starting obstacles"""
            self.driver.implicitly_wait(3)
            self.click_on_element("btnEulaAgree")
            self.click_on_element("welcomeScreenBtnYes")
            self.flow_from_signin()
            self.driver.implicitly_wait(30)  ##waiting for signin
            self.click_on_flag_element("ribbon")
            self.flow_from_choose_walabot()
            self.flow_from_connection()
        except (FlagElementCouldNotFound, InsideElementError):
            raise InsideElementError

    def flow_from_connection(self):

        self.sometimes_appears()
        """Here is The connection To walabot"""
        self.driver.implicitly_wait(35)

        """This line is very important, it checks if the connectivity process happened"""
        try:self.click_on_flag_element("done")
        except FlagElementCouldNotFound:
            raise InsideElementError

        self.device.prog_bar.step()

        self.click_on_complex("rippleBackgroundAnimation", "Middle")
        self.driver.implicitly_wait(10)
        time.sleep(2)
        self.driver.press_keycode(4)
        self.driver.press_keycode(AndroidKey.BACK)
        self.click_on_element("noButton")
        temp_string = '/hierarchy/android.widget.FrameLayout/' \
                      'android.widget.LinearLayout/' \
                      'android.widget.FrameLayout/android.widget.RelativeLayout/' \
                      'android.widget.RelativeLayout/android.widget.RelativeLayout/' \
                      'android.widget.ImageView[4]'

        self.driver.find_element(AppiumBy.XPATH, temp_string).click()

        try:
            self.driver.find_element(AppiumBy.ID, f"{self.app_package}:id/startScan").click()
        except NoSuchElementException:
            raise InsideElementError
        """if everything worked FINE"""
        raise ScanInProgress


    def flow_from_signin(self):
        """
        This function is to start the navigation from the sign-in page.
        :return:
        """
        self.driver.implicitly_wait(6)
        self.click_on_complex("alreadyHaveAccount", "Right")

        try:
            self.send_keys_element("etEmail", "appiumtest@gmail.com")
            self.click_on_element("next")
            self.send_keys_element("etPassword", "password")
            self.click_on_element("next")
            self.device.prog_bar.step()

        except Exception as e:
            self.context_logger.debug(str(e))
            raise SignInError

    def flow_from_choose_walabot(self):

        self.driver.implicitly_wait(6)
        self.click_on_element("start")
        self.click_on_element("continueBtn")
        self.click_on_element("qr_not_found")
        self.click_on_element("enter_network_name")

        try:
            self.send_keys_element("ssid_input_1", str(self.walabot_ssid[0]))
            self.send_keys_element("ssid_input_2", str(self.walabot_ssid[1]))
            self.send_keys_element("ssid_input_3", str(self.walabot_ssid[2]))
            self.click_on_element("ok_button")

        except AttributeError:
            raise InsideElementError

        """Location Permission button"""
        if (int(self.device.os_string) < 10):
            try:
                self.driver.implicitly_wait(3)
                self.click_on_element("button1", True)
                self.driver.find_element(AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button").click()
                self.context_logger.info("Permission Allow Button Clicked")
            except NoSuchElementException:
                pass

        ###Add This
        ##com.walabot.test:id/wifiAnimation

    def sometimes_appears(self):
        """ This function bundles the connection buttons which often appears and often not."""

        self.driver.implicitly_wait(6)
        self.click_on_element("okButton")
        self.driver.implicitly_wait(4)
        self.click_on_element("connect")
        self.driver.implicitly_wait(15)

        """There is a difference in connection between different OS versions. """
        if (int(self.device.os_string) > 10):
            self.click_on_element("button1", True)
        else:
            self.click_on_element("icon", True)

        ##reconnectButton

        """OTA FLOW """
        try:

            self.click_on_flag_element("connect")
            self.driver.implicitly_wait(30)
            self.click_on_element("connect")
        except FlagElementCouldNotFound:
            pass

            ##com.walabot.test:id/rippleBackgroundAnimation
            ###com.walabot.test:id/scanModesLocator

            # self.driver.press_keycode(AndroidKey.BACK)
            # self.click_on_complex("scanModesLocator","Middle-Left")


    def click_on_element(self, element_id, android=False):
        """
        This function Looks for Element and then click on him, if she doesn't find the element it moves on.
        :param element_id:"The Element ID"
        :param android: Default is False, When true the package is set to be android, for pressing OS Elements
        :return:
        """
        if android:
            try:
                self.driver.find_element(AppiumBy.ID, f"android:id/{element_id}").click()
                self.context_logger.info(f"OS {element_id} Clicked")
                return
            except NoSuchElementException:
                if element_id == "button1":
                    self.context_logger.debug(f"Could Not Find OS Connect button, Check if there is connectivity error")
                else:
                    self.context_logger.debug(f"Could Not Find OS {element_id}")
                return
        else:
            try:
                self.driver.find_element(AppiumBy.ID, f"{self.app_package}:id/{element_id}").click()
                self.context_logger.info(f"{element_id} Clicked")
                return
            except NoSuchElementException:
                self.context_logger.debug(f"Could Not Find {element_id}")
                return


    def click_on_flag_element(self, element_id):
        """
        This function is simillar to Click on element function but it raise FlagElementCouldnot Found if it doesn't find the
        element, it is designed for elements that usually appear when first opening the app.
        :param element_id:
        :return:
        """
        try:
            self.driver.find_element(AppiumBy.ID, f"{self.app_package}:id/{element_id}").click()
            self.context_logger.info(f"{element_id} Clicked")
            return
        except NoSuchElementException:
            self.context_logger.debug(f"Flag Element:Could Not Find {element_id}")
            raise FlagElementCouldNotFound

    def send_keys_element(self, element_id, key):
        try:
            self.driver.find_element(AppiumBy.ID, f"{self.app_package}:id/{element_id}").send_keys(key)
            self.context_logger.info(f"{element_id} keys Sent with Value [{key}]")
            return
        except NoSuchElementException:
            self.context_logger.debug(f"Could Not Find {element_id}")
            return

    def click_on_complex(self, element_id, side):
        """
        This function Attempt to click on elements that are more complex, elements that are hidden
        and could not be found by regular element search.
        :param element_id:The element Id
        :param side:Right side or middle side, where the click should occur.
        :return:if the action fail, the function will raise flag Error so the session will end
        """
        try:
            location_dict = self.driver.find_element(AppiumBy.ID, f"{self.app_package}:id/{element_id}").location
            elememt_dimension = self.driver.find_element(AppiumBy.ID, f"{self.app_package}:id/{element_id}").size

            if side == "Middle":
                index_x = int(elememt_dimension["width"] / 2) + location_dict["x"]
                index_y = int(elememt_dimension["height"] / 2) + location_dict["y"]
                self.driver.tap([(index_x, index_y)], 800)

            elif side == "Middle-Left":
                index_x = int(elememt_dimension["width"] / 4) + location_dict["x"]
                index_y = location_dict["y"] - int(elememt_dimension["height"] / 1.3)
                print(location_dict)
                print(elememt_dimension)
                print(index_y)
                print(index_x)
                self.driver.tap([(index_x, index_y)], 800)

            elif side == "Right":
                index_x = elememt_dimension["width"] + location_dict["x"] - 30
                index_y = elememt_dimension["height"] + location_dict["y"] - 20
                self.driver.tap([(index_x, index_y)], 300)

            self.context_logger.info(f"Complex Element: Clicked On- {element_id}")
            return True

        except NoSuchElementException:
            self.context_logger.debug(f"Complex Element: Could not find the  {element_id}")
            raise InsideElementError

    def start_logger(self):

        """Starting Logger"""
        date_val = datetime.today().strftime('%d-%m-%Y')
        self.time_val = datetime.today().strftime("%H:%M:%S")

        """Clean all multiple loggers"""
        for i in range(15):
            try:
                logger.remove(i)
            except ValueError:
                pass

        """Bind the device name"""
        try:
            logger.add(self.device.folder_path + f"\\{date_val}-log.txt",
                       format="{time:HH:mm:ss.SS} | {level:<8} | {extra[id]:<14} |                        {message}")

            self.context_logger = logger.bind(id=self.device.device_real_name)
            self.context_logger.info(f"++++++++++++++++{date_val}+++++{self.time_val}++++++++++++++++")
            self.context_logger.info(f"{self.device.apk_path}- Was chosen as path to APK")
            return
        except PermissionError:
            pass

    # def change_prog_bar(self, color=None, value=None, message=None):
    #
    #     if value:
    #         self.device.prog_bar['value'] = value
    #     else:
    #         self.device.prog_bar.step(self.stepper)
    #
    #     if color and message:
    #         self.device.prog_bar_style.configure(f"p{self.device.device_number}.LabeledProgressbar", foreground='black',
    #                                              background=color, text=f"{message}     ")
    #     elif message:
    #         self.device.prog_bar_style.configure(f"p{self.device.device_number}.LabeledProgressbar",
    #                                              text=f"{message}     ")

# def advance_progressbar(func):
#     def wrapper(*args):
#         func()
#         print("Something is happening after the function is called.")
#
#     return wrapper
# choosen_folder=r"C:\Users\GuyLeiba\Documents\Projtesting"
# app_package = "com.walabot.vayyar.ai.plumbing"
# app_apk=r'C:\Users\GuyLeiba\Documents\Projtesting\inwall-prod-sensor-release-3.14.02_fixing_v3.14.0-d7ab352e0_WalabotDIY_2022.01.20_v3.0.26-3cc704c8.apk'
# apk="C:\\Users\\GuyLeiba\\Documents\\Projtesting\\inwall-prod-sensor-release-3.14.02_fixing_v3.14.0-d7ab352e0_WalabotDIY_2022.01.20_v3.0.26-3cc704c8.apk"
# devlogname="new.txt"
#
# dict1={
#     "apk_path":apk,
#     "folder":choosen_folder,
#     "app_package":app_package,
#     "deviceid":"R58M20NGMAN",
#     "port_num":8202,
#     "walabot_ssid":801_402_666,
#     "devlogname":"bals",
#     "cool_time":3,
#     "run_number":2
# }
# test1=Tester(dict1)
# test1.start_test()


# #test2=Tester(apk,choosen_folder,app_package,deviceid="R5CN308Z4SE",port_num=8205)
#
# # print(test1.app_package)
# # e=test1.start_test()
# b=test1.start_test()
# test1.fin()
# #print(e)


#
# def main_session(app_package, apk_path, choosen_folder,devlogname):
#
#     #ANDROID_BASE_CAPS=get_base_caps(app_package,apk_path)
#     driver = webdriver.Remote("http://localhost:4723/wd/hub", ANDROID_BASE_CAPS)  ##create session
#
#     print(driver.is_app_installed(app_package))
#     print(driver.is_app_installed("com.walabot.test"))

# activity = "com.walabot.vayyar.ai.plumbing.presentation.IntroActivity"
# driver.start_activity(app_package,activity)
# driver.launch_app()

# app_package="com.walabot.test"

# driver.find_element(AppiumBy.ID, "com.walabot.vayyar.ai.plumbing:id/btnEulaAgree").click()
#
# driver.implicitly_wait(30)
# time.sleep(10)
# driver.quit()
# guidence_nav(driver,app_package)
#     driver.implicitly_wait(120)
#     time.sleep(20)
#     status=fin(driver,app_package,choosen_folder,devlogname)
#     return status
# except Exception as e:
#     return e


# if __name__ == "__main__":


# def which_apk_installed(driver,package):
#     driver.is_app_installed('com.example.AppName');

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
