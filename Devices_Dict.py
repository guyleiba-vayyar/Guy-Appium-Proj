class FieldsEmptyError(Exception):
    """Raised when the the device fields arn't full"""
    pass

class BadApkName(Exception):
    """Raised when the user changed the original"""
    pass

class ApkNFolderError(Exception):
    """Raised when the apk and the folder fields arn't full"""
    pass

class SSIDError(Exception):
    """Raised when SSID Number is Too large or too small"""
    pass

class InsideElementError(Exception):
    """Raised when can't find inside element(meaning function is already running"""
    pass

class FlagElementCouldNotFound(Exception):
    """Raised when can't find The first element (like elements that first appear when opening the app"""
    pass

class ScanInProgress(Exception):
    """Raised when can't find The first element (like elements that first appear when opening the app"""
    pass

class SignInError(Exception):
    """
    Raised when appium could not find the sign in button, maybe the device dimensions are different
    needs developer attention probably
    """
    pass

class AppiumConnectionError(Exception):
    """
    Raised when appium server is down
    """
    pass

udid_dict={

    "R58M20NGMAN":"Galaxy_S10+",
    "R5CN308Z4SE":"Galaxy_S20+",
    "R5CT30J0HED":'Demo_Device'
}

ssid_dict={
    1: "223000365",
    2: "224007088",
    3: "223000050",
    4: "223000563",
    5: "116039926"

}
num_dict={
    1: "1st-Run",
    2: "2nd-Run",
    3: "3rd-Run",
    4: "4th-Run"
}