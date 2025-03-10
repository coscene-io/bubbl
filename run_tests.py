#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest
import os
from tests import testcases

"""批量执行PlaywRight框架录制的界面自动化测试Case"""
all_cases_path = testcases("./tests/testcases")

if __name__ == '__main__':
    pytest.main(['-s', '-q','./', '--clean-alluredir', '--alluredir=allure-results'])
    os.system('cp environment.properties ./allure-results/environment.properties')
    os.system("allure generate -c -o allure-report")