# main.py
import unittest
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class ColorTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(Fore.GREEN + f"SUCCESS: {test}")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.writeln(Fore.RED + f"ERROR: {test}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln(Fore.RED + f"FAILURE: {test}")

class ColorTextTestRunner(unittest.TextTestRunner):
    resultclass = ColorTextTestResult

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("verbosity", 2)
        super().__init__(*args, **kwargs)



if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = ColorTextTestRunner()
    runner.run(suite)