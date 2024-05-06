import logging
import os
from typing import Type

from injector import Injector
from pytest import FixtureRequest
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webdriver import WebDriver

from .module import Module
from .router import Router


class Application:
    container: Injector
    testrun_uid: str
    request: FixtureRequest
    driver: WebDriver
    options: any
    e2e_enabled: bool = False
    closed: bool = False

    def __init__(self, params: dict):
        logging.info("Creating application")

        options = params.get("options")
        self.request = params.get("request")
        self.driver = params.get("driver")
        self.testrun_uid = params.get("testrun_uid")
        self.container = Injector()
        self.router = Router()

        routes = params.get("routes")

        if options:
            self.options = options
        else:
            self.options = {}

        self.__configure_log__()
        self.register_routes(routes)

    def init_e2e(self):
        if self.e2e_enabled:
            return

        self.e2e_enabled = True

        self.driver = self.__init_driver__()

        self.closed = False

    def is_e2e_enabled(self):
        return self.e2e_enabled

    def get(self, key: any):
        return self.container.get(key)

    def register_module(self, module_class: Type[Module]):
        module = module_class(self)
        self.container.binder.bind(module_class, module)

    def register_routes(self, routes: dict):
        self.router.register_routes(routes)

    def go_to(self, key: str):
        if not self.e2e_enabled:
            return

        return self.router.get_page(self, key)

    def close(self):
        if self.closed:
            return

        logging.info("Closing application")

        if self.is_e2e_enabled():
            self.driver.quit()
            logging.info("Driver closed")

        self.e2e_enabled = False
        self.closed = True

        logging.info("Application closed")

    def __configure_log__(self):
        worker_id = os.environ.get("PYTEST_XDIST_WORKER")
        if worker_id is not None:
            with open(file=f"logs/pytest_{worker_id}.log", mode="w", encoding="utf-8"):
                pass

            logging.basicConfig(
                format=self.request.getini("log_file_format"),
                filename=f"logs/pytest_{worker_id}.log",
                level=self.request.getini("log_file_level"),
            )

    def __init_driver__(self) -> WebDriver:
        logging.info("Initializing driver")
        selenium_cmd_executor = os.environ.get(
            "SELENIUM_CMD_EXECUTOR", "http://selenium:4444/wd/hub"
        )
        implicitly_wait_time = self.options.get("implicitly_wait_time", 10)
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = Remote(command_executor=selenium_cmd_executor, options=options)
        driver.implicitly_wait(implicitly_wait_time)
        logging.info("Driver initialized")

        return driver
