import datetime
import time
import subprocess
from datetime import datetime
from subprocess import check_output


class Android_Connector():

    def __init__(self, webdriver,app_package,device,logger):
        self.app_package= app_package
        self.webdriver=webdriver
        self.device=device
        self.context_logger=logger

        self.set_the_caps()


    def remove_current_app(self):

        try:
            try_driver = self.webdriver.Remote("http://localhost:4723/wd/hub", self.prod_caps)
            time.sleep(10)
            try_driver.remove_app("com.walabot.vayyar.ai.plumbing")
            self.local_server_kill(try_driver)

        except Exception:
            time.sleep(10)
            try_driver = self.webdriver.Remote("http://localhost:4723/wd/hub", self.test_caps)
            try_driver.remove_app("com.walabot.test")
            """App Recover Time"""
            time.sleep(10)
            self.local_server_kill(try_driver)


    def appium_connection_helper(self,caps):
        """An helper function that connects to the right package"""

        try:
            try_driver = self.webdriver.Remote("http://localhost:4723/wd/hub", caps)
            return try_driver

        except Exception as e:
            self.context_logger.error(f"Connection Fail")
            return False



    def create_connection(self,run_number):
        """
        This is the main class function, it creates the connection
        :return appium server driver.
        """

        """
        This function is the main connection function, it starts by checking if a different app type is already installed,
        on the device,if so it uses two helper functions that removes the app and then initializes regular connection.
        """

        if run_number==1:
            self.remove_current_app()

        if self.app_package=="com.walabot.test":
            self.test_caps["app"] = self.device.apk_path
            driver=self.appium_connection_helper(self.test_caps)

        elif self.app_package=="com.walabot.vayyar.ai.plumbing":
            self.prod_caps["app"] = self.device.apk_path
            driver=self.appium_connection_helper(self.prod_caps)

        if driver:return driver


    def fin(self,driver,testnum=None,test_indicator=False):
        """
        This function concludes the Test it recieves test_indicator as false in default,
        if test were succeed then it will ve true and then it will pull the devlog
        """

        if test_indicator:
            self.pull_devlog()
            self.delete_devlog()

        if (testnum==self.device.desired_run_num) and test_indicator:
            self.device.change_prog_bar("green",100,"Success!")
            self.device.start_btn.config(state='enabled')

        elif (testnum==self.device.desired_run_num) and not test_indicator:
            self.device.change_prog_bar("yellow",100,"Partial Success, Check logs!")
            self.device.start_btn.config(state='enabled')

        self.context_logger.trace(f"Closing Connection")

        try:
            driver.close_app()
            driver.quit()

        except Exception:
            self.context_logger.trace(f"404 Couldn't close connection")

    def local_server_kill(self,driver):
        try:
            driver.close_app()
            driver.quit()
        except Exception:
            self.context_logger.trace(f"404 Couldn't close connection")


    def pull_devlog(self):
        """
        This function pulls the devlog,it sets the new path and using the adb pull command it pullsit
        Note!
        The function that is in charge on the devlog name is on the main.py file do not change the devlogname from here.
        """
        date_val = datetime.today().strftime('%d-%m-%Y')
        time_val = datetime.today().strftime("%H-%M-%S")

        new_devlog_name=f"[{date_val}-{time_val}]-{self.device.devlog_name}"
        newpath = f"{self.device.folder_path}/{new_devlog_name}.txt"

        print(newpath)
        adb_pullcommand = f"adb -s {self.device.udid_val} pull /sdcard/Android/data/{self.app_package}/files/devLog.txt {newpath}"
        print(adb_pullcommand)
        try:
            out = check_output(adb_pullcommand.split())
            if "1 file pulled" in str(out):
                self.context_logger.info(f"Devlog.txt Was successfuly pulled")
            else:
                self.context_logger.error(f"Devlog.txt Was NOT FOUND")
        except Exception:
            self.context_logger.error(f"ADB Pull Command ERROR")


    def delete_devlog(self):
        adb_del_command = f"adb -s {self.device.udid_val} shell rm /sdcard/Android/data/{self.app_package}/files/devlog.txt"
        subprocess.call(adb_del_command, shell=True)


    def set_the_caps(self):

        port_num= 8204+(self.device.device_number*2)
        base_caps = {

            "appium:udid": self.device.udid_val,
            "appium:systemPort": port_num,
            "platformName": "Android",
            "appium:automationName": "uiautomator2",
            "appium: autoLaunch": "false",
            "appium:newCommandTimeout": 130,
            "appActivity": "com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
            "noReset": "true",
            "fullReset": "false"
        }


        self.test_caps = base_caps.copy()
        self.test_caps["appium:appPackage"] = "com.walabot.test"
        self.test_caps["appium:systemPort"] = port_num + 1

        self.prod_caps = base_caps.copy()
        self.prod_caps["appium:appPackage"] = "com.walabot.vayyar.ai.plumbing"

        self.context_logger.info(f"loaded BASE CAPS{base_caps}")
