# import pytest
# from playwright.sync_api import sync_playwright
#
# @pytest.fixture(scope="session")
#
# def pytest_addoption(parser):
#     """
#     添加命令行选项 --cn-jwt，用于传递 JWT Token。
#     """
#     parser.addoption(
#         "--cn-jwt",
#         action="store",
#         default=None,
#         help="JWT Token for authentication",
#     )
# def browser_context(pytestconfig):
#     """
#     初始化 Playwright 浏览器上下文，并设置通用的 JWT Token 和 localStorage。
#     """
#     # Access configuration options using pytestconfig
#     jwt_token = pytestconfig.getoption("--cn-jwt")
#     if not jwt_token:
#         raise ValueError("--cn-jwt option is required but not provided")
#
#     # 启动 Playwright
#     playwright = sync_playwright().start()
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#
#     # 设置 localStorage
#     context.add_init_script(f"""
#         localStorage.setItem('coScene_org_jwt', '{jwt_token}');
#         localStorage.setItem('i18nextLng', 'cn');
#     """)
#
#     # 返回上下文供测试用例使用
#     yield context
#
#     # 测试结束后清理资源
#     context.close()
#     browser.close()