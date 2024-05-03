import threading
import traceback
import datetime

from .base_testcase import BaseTestCase


class StartTestcaseThread(threading.Thread):
    """
    The StartTestcaseThread is designed to invoke the testcase's runTest() or run_test() method.
    Upon successful execution without any exceptions, it will set the testcase's done_flag to "True" to indicate completion.

    @author: Wang Lin
    """

    def __init__(self, executing_testcase):
        threading.Thread.__init__(self)
        self.executing_testcase = executing_testcase

    def run(self):
        # First, execute the setup() method, followed by the run_test() method.

        self.executing_testcase.testcase_start_time = datetime.datetime.now()

        try:
            # Before executing the setup() method, log TestEngineCaseInput if the action is initiated by the test-engine.
            if BaseTestCase.TestEngineCaseInput:
                self.executing_testcase.logger.info("------ TestEngineCaseInput:")
                self.executing_testcase.logger.info(self.executing_testcase.TestEngineCaseInput)

            if hasattr(self.executing_testcase, "setup"):
                self.executing_testcase.logger.info("------ execute setup() Start")
                self.executing_testcase.setup()
                self.executing_testcase.logger.info("------ execute setup() End")

            if hasattr(self.executing_testcase, "runTest"):
                print("The method runTest() is deprecated. Please rename it to run_test().")
                self.executing_testcase.logger.info("================== runTest() start:")
                self.executing_testcase.runTest()
            else:
                self.executing_testcase.logger.info("================== run_test() start:")
                self.executing_testcase.run_test()
        except BaseException:
            if hasattr(self.executing_testcase, "exception_info"):
                print("already Timeout, no need to log exception_info again")
            else:
                traceback.print_exc()
                self.executing_testcase.exception_info = traceback.format_exc()
        else:
            self.executing_testcase.done_flag = True
