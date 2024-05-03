import os
import platform
import traceback
import subprocess
from selenium import webdriver

from .webdriver_wrapper_firefox import WebDriverWrapperFireFox
from .webdriver_wrapper_edge import WebDriverWrapperEdge
from .webdriver_wrapper_chrome import WebDriverWrapperChrome
from .webdriver_wrapper_safari import WebDriverWrapperSafari
from .webdriver_wrapper_ie import WebDriverWrapperIE

try:
    import settings
except ImportError:
    traceback.print_exc()

try:
    if hasattr(settings, "run_by_github_action") and settings.run_by_github_action is True:
        pass
    else:
        try:
            from settings import auto_download_chromedriver
        except ImportError:
            auto_download_chromedriver = False

        if auto_download_chromedriver is True:
            import chromedriver_autoinstaller

            chromedriver_autoinstaller.install()
except BaseException:
    traceback.print_exc()


class SeleniumHelper(object):
    set_implicitly_wait_flag = False

    @staticmethod
    def open_browser(ui_testcase=None, browser_name=None):
        if browser_name is None:
            if hasattr(settings, "DefaultBrowserName"):
                browser_name = settings.DefaultBrowserName
            elif hasattr(ui_testcase, "DefaultBrowserName"):
                browser_name = ui_testcase.DefaultBrowserName
            else:
                browser_name = "chrome"

        browser_name = browser_name.lower()

        ui_testcase.browser_name = browser_name

        if hasattr(settings, "token") and settings.token:
            # todo: 1. 如果settings.token 存在，则所有UI case 都使用此 token ?  2.  此处先实现功能为主，暂时只支持 Chrome
            if browser_name == 'chrome':
                from seleniumwire import webdriver  # Import from seleniumwire
                browser = webdriver.Chrome()

                def interceptor(request):
                    request.headers['authorization'] = "Bearer %s" % settings.token

                browser.request_interceptor = interceptor

                return browser

        elif hasattr(ui_testcase, "token"):
            if browser_name == 'chrome':
                from seleniumwire import webdriver  # Import from seleniumwire
                browser = webdriver.Chrome()

                def interceptor(request):
                    request.headers['authorization'] = "Bearer %s" % ui_testcase.token

                browser.request_interceptor = interceptor

                return browser

        else:
            from selenium import webdriver

            if browser_name == 'ie':
                    browser = WebDriverWrapperIE(ui_testcase)
            elif browser_name == 'edge':
                if hasattr(settings, "HEAD_LESS") and settings.HEAD_LESS:
                    edge_options = webdriver.EdgeOptions()
                    edge_options.add_argument("--headless")

                    # 使用 WebDriverWrapperEdge 替换原来的 webdriver 实例
                    browser = WebDriverWrapperEdge(ui_testcase, options=edge_options)
                else:
                    browser = WebDriverWrapperEdge(ui_testcase)

            elif browser_name == 'safari':
                    browser = WebDriverWrapperSafari(ui_testcase)

            elif browser_name == 'chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--disable-infobars")

                if hasattr(settings, "BROWSER_OPTION"):
                    for opt in settings.BROWSER_OPTION:
                        if type(opt) is str:
                            chrome_options.add_argument(opt)
                        else:
                            raise Exception("settings.BROWSER_OPTION must be a string list!")

                if ui_testcase is None:
                    # read setting.HEAD_LESS 如存在并且值为True 则使用无头模式 否则使用有头模式
                    if hasattr(settings, "HEAD_LESS") and settings.HEAD_LESS:
                        # from selenium.webdriver.chrome.options import Options
                        chrome_options.add_argument("--headless")
                        chrome_options.add_argument("--disable-gpu")
                        chrome_options.add_argument("--no-sandbox")
                        chrome_options.add_argument("--disable-dev-shm-usage")
                        browser = webdriver.Chrome(chrome_options=chrome_options)
                    else:
                        browser = webdriver.Chrome(chrome_options=chrome_options)
                else:
                    if hasattr(settings, "HEAD_LESS") and settings.HEAD_LESS:
                        # from selenium.webdriver.chrome.options import Options
                        chrome_options.add_argument("--headless")
                        chrome_options.add_argument("--disable-gpu")
                        chrome_options.add_argument("--no-sandbox")
                        chrome_options.add_argument("--disable-dev-shm-usage")
                        # 使用 WebDriverWrapperChrome 替换原来的 webdriver 实例
                        browser = WebDriverWrapperChrome(ui_testcase, options=chrome_options)
                    else:
                        # browser = webdriver.Chrome()
                        # 使用 WebDriverWrapperChrome 替换原来的 webdriver 实例
                        browser = WebDriverWrapperChrome(ui_testcase)

            elif browser_name in ('firefox', 'ff'):
                if hasattr(settings, "HEAD_LESS") and settings.HEAD_LESS:
                    firefox_options = webdriver.FirefoxOptions()
                    firefox_options.add_argument("--headless")

                    # 使用 WebDriverWrapperFireFox 替换原来的 webdriver 实例
                    browser = WebDriverWrapperFireFox(ui_testcase, options=firefox_options)
                else:
                    browser = WebDriverWrapperFireFox(ui_testcase)





            elif browser_name == 'device':
                from appium import webdriver as mobiledriver
                browser = mobiledriver.Remote(
                    command_executor='http://' + ui_testcase.appium_server_ip + ':' + ui_testcase.appium_server_port
                                     + '/wd/hub', desired_capabilities=ui_testcase.capability)

        try:
            browser.maximize_window()
        except BaseException:
            traceback.print_exc()

        if SeleniumHelper.set_implicitly_wait_flag is False:
            # user can set the "WEBDRIVER_IMPLICIT_WAIT" in settings.
            # eg: WEBDRIVER_IMPLICIT_WAIT = 60
            # if there are no WEBDRIVER_IMPLICIT_WAIT found in settings, then set a default value: 20 (in seconds)
            if hasattr(settings, "WEBDRIVER_IMPLICIT_WAIT"):
                if type(settings.WEBDRIVER_IMPLICIT_WAIT) == int or type(settings.WEBDRIVER_IMPLICIT_WAIT) == float:
                    browser.implicitly_wait(settings.WEBDRIVER_IMPLICIT_WAIT)
                    print("set WEBDRIVER_IMPLICIT_WAIT: %s" % settings.WEBDRIVER_IMPLICIT_WAIT)
                else:
                    # if the type of settings.WEBDRIVER_IMPLICIT_WAIT is not correct, here set a default value: 20
                    browser.implicitly_wait(20)
                    print(
                        "the type of WEBDRIVER_IMPLICIT_WAIT:%s is not 'int' or 'float', here set a default value: 20")
            else:
                # if there are no WEBDRIVER_IMPLICIT_WAIT found in settings, then set a default value: 20
                browser.implicitly_wait(20)
                print(
                    "there are no WEBDRIVER_IMPLICIT_WAIT found in settings, then set a default value: 20")

            # set SeleniumHelper.set_implicitly_wait_flag = True after set the WEBDRIVER_IMPLICIT_WAIT.
            SeleniumHelper.set_implicitly_wait_flag = True

        return browser

    @staticmethod
    def switch_to_new_window(browser, old_handle_list=None):
        """
        this is used to switch to new window.
        Note: if there are only two windows, the old_handle_list can be the default value: None, the new window will be selected.
              if there are more than two windows, the old_handle_list should be the list of older window's handle, the new window will be selected
        """
        old_handle = browser.current_window_handle
        handles = browser.window_handles

        for handle in handles:
            if old_handle_list == None:
                if handle == old_handle:
                    print("%s is the old window's handler" % (handle))
                else:
                    print("%s is the new window's handler" % (handle))
                    break
            else:
                if handle in old_handle_list:
                    print("%s is the old window's handler" % (handle))
                else:
                    print("%s is the new window's handler" % (handle))
                    break

        browser.switch_to_window(handle)
