import os
import shutil

import pytest

if __name__=="__main__":
    alluredir="./temp"
    reports_dir="./report"
    pytest.main(["--alluredir",alluredir,"--clean-alluredir"])
    os.system(f"allure generate {alluredir} -o {reports_dir} --clean")
    shutil.copy2("environment.properties","temp")